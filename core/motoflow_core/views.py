import logging
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, Q
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

logger = logging.getLogger(__name__)
from .models import Cliente, Motocicleta, OrdenTrabajo, EventoMuro, Cotizacion, ItemCotizacion
from .serializers import ClienteSerializer, MotocicletaSerializer, OrdenTrabajoSerializer, EventoMuroSerializer, SeguimientoOrdenSerializer, CotizacionSerializer
import os
import requests
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, JSONParser
import json as json_module
from rest_framework.response import Response
from .whatsapp_service import WhatsAppService # Importamos el servicio que creamos

class SeguimientoClienteView(generics.RetrieveAPIView):
    queryset = OrdenTrabajo.objects.all()
    serializer_class = SeguimientoOrdenSerializer
    lookup_field = 'hash_seguimiento'
    permission_classes = [AllowAny]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class MotocicletaViewSet(viewsets.ModelViewSet):
    queryset = Motocicleta.objects.all()
    serializer_class = MotocicletaSerializer

class OrdenTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.all()
    serializer_class = OrdenTrabajoSerializer

class EventoMuroViewSet(viewsets.ModelViewSet):
    queryset = EventoMuro.objects.all() 
    serializer_class = EventoMuroSerializer

    def get_queryset(self):
        # Tomamos todos los eventos
        queryset = EventoMuro.objects.all()
        
        # Filtramos por la orden si el frontend lo solicita
        orden_id = self.request.query_params.get('orden', None)
        if orden_id is not None:
            queryset = queryset.filter(orden_id=orden_id)
            
        return queryset

# --- VISTA: REGISTRO FINAL CON WHATSAPP ---
@api_view(['POST'])
def registrar_ingreso_moto(request):
    """
    Recibe los datos del formulario de Vue, guarda en DB y envía WhatsApp.
    """
    datos = request.data
    placa = datos.get('placa', '').upper()
    nombre = datos.get('nombre')
    celular = datos.get('celular')
    modelo = datos.get('modelo')

    # --- FORMATEO DE CELULAR (Ecuador) ---
    if celular.startswith('0'):
        celular = '593' + celular[1:]
    elif not celular.startswith('593'):
        celular = '593' + celular

    try:
        # 1. Crear o actualizar el Cliente
        cliente, _ = Cliente.objects.get_or_create(
            celular=celular,
            defaults={'nombre': nombre}
        )

        # 2. Crear o actualizar la Motocicleta
        moto, _ = Motocicleta.objects.get_or_create(
            placa=placa,
            defaults={'modelo': modelo, 'propietario': cliente}
        )

        # 3. Crear la Orden de Trabajo (El ingreso al taller)
        orden = OrdenTrabajo.objects.create(
            moto=moto,
            estado='taller'
        )

        # 4. ENVÍO DE WHATSAPP
        ws = WhatsAppService()
        resultado_ws = ws.enviar_mensaje_bienvenida(
            numero_cliente=celular,
            nombre_cliente=nombre,
            placa_moto=placa,
            hash_seguimiento=str(orden.hash_seguimiento)
        )

        return Response({
            'status': 'success',
            'mensaje': 'Moto ingresada y WhatsApp enviado',
            'orden_id': orden.id,
            'hash_seguimiento': orden.hash_seguimiento,
        })

    except Exception as e:
        logger.error('registrar_ingreso_moto: %s', e)
        return Response({'error': 'Error interno al registrar la moto'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def probar_conexion_ia(request):
    try:
        respuesta_fastapi = requests.get('http://ai_service:8001/')
        return Response({
            "estado_django": "Excelente",
            "mensaje": "¡Los contenedores están hablando entre ellos!",
            "respuesta_desde_fastapi": respuesta_fastapi.json()
        })
    except Exception as e:
        logger.error('probar_conexion_ia: %s', e)
        return Response({"estado_django": "Error", "mensaje": "No se pudo conectar al servicio de IA"}, status=500)

@api_view(['POST'])
def procesar_nota_voz(request):
    if 'audio' not in request.FILES:
        return Response({'error': 'No se envió ningún audio'}, status=400)
    
    orden_id = request.data.get('orden_id')
    audio_file = request.FILES['audio']
    archivos_para_fastapi = {'audio': (audio_file.name, audio_file.read(), audio_file.content_type)}
    
    try:
        res_trans = requests.post('http://ai_service:8001/api/transcribir/', files=archivos_para_fastapi)
        texto = res_trans.json().get('texto', '')
        res_check = requests.post('http://ai_service:8001/api/estructurar-checklist/', json={"texto": texto})
        checklist = res_check.json()
        tareas = checklist.get('tareas', [])
        
        eventos_creados = []
        for tarea in tareas:
            descripcion_tarea = tarea.get('descripcion', 'Tarea sin nombre') if isinstance(tarea, dict) else str(tarea)
            nuevo_evento = EventoMuro.objects.create(orden_id=orden_id, tipo='tarea', contenido_texto=descripcion_tarea)
            

            evento_serializado = EventoMuroSerializer(nuevo_evento).data
            print(f"🟢 EVENTO SERIALIZADO: {evento_serializado}")

            eventos_creados.append(EventoMuroSerializer(nuevo_evento).data)

            print(f"🔵 PAQUETE FINAL A ENVIAR: eventos_guardados tiene {len(eventos_creados)} elementos")

        return Response({'transcripcion': texto, 'checklist': tareas, 'eventos_guardados': eventos_creados})
    except Exception as e:
        logger.error('procesar_nota_voz: %s', e)
        return Response({'error': 'Error al procesar la nota de voz'}, status=500)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def escanear_placa(request):
    imagen = request.FILES.get('imagen')
    if not imagen:
        return Response({'error': 'No se envió ninguna foto'}, status=400)

    try:
        files = {'file': (imagen.name, imagen.read(), imagen.content_type)}
        respuesta_ia = requests.post('http://ai_service:8001/api/leer-placa/', files=files)
        placa = respuesta_ia.json().get('placa_detectada')

        if not placa:
            return Response({'error': 'No se pudo leer la placa'}, status=400)

        try:
            moto = Motocicleta.objects.get(placa=placa)
            return Response({
                'placa': placa, 'existe': True,
                'datos': {
                    'modelo': moto.modelo,
                    'nombre': moto.propietario.nombre,
                    'celular': '0' + moto.propietario.celular[3:] if moto.propietario.celular.startswith('593') else moto.propietario.celular,
                }
            })
        except Motocicleta.DoesNotExist:
            return Response({'placa': placa, 'existe': False})
    except Exception as e:
        logger.error('escanear_placa: %s', e)
        return Response({'error': 'Error al procesar la imagen'}, status=500)
    
@api_view(['POST'])
def finalizar_orden(request):
    """
    Marca la orden como 'lista' y envía WhatsApp de aviso de retiro.
    """
    orden_id = request.data.get('orden_id')
    if not orden_id:
        return Response({'error': 'Falta el ID de la orden'}, status=400)

    try:
        # 1. Buscamos la orden
        orden = OrdenTrabajo.objects.get(id=orden_id)
        
        # 2. Cambiamos el estado
        orden.estado = 'lista'
        total = request.data.get('total_cobro')
        if total is not None:
            orden.total_cobro = total
        orden.save()

        # 3. Agregamos un hito oficial en el muro
        EventoMuro.objects.create(
            orden=orden,
            tipo='tarea',
            contenido_texto=f'✅ Trabajo finalizado. La motocicleta está lista para entrega.'
        )

        # 4. ENVÍO DE WHATSAPP AL CLIENTE
        ws = WhatsAppService()
        cliente = orden.moto.propietario
        resultado_ws = ws.enviar_mensaje_moto_lista(
            numero_cliente=cliente.celular,
            nombre_cliente=cliente.nombre,
            placa_moto=orden.moto.placa,
            hash_seguimiento=str(orden.hash_seguimiento)
        )

        return Response({
            'status': 'success',
            'mensaje': 'Orden finalizada y cliente notificado.',
        })
    except OrdenTrabajo.DoesNotExist:
        return Response({'error': 'Orden no encontrada'}, status=404)
    except Exception as e:
        logger.error('finalizar_orden: %s', e)
        return Response({'error': 'Error al finalizar la orden'}, status=500)

# --- NUEVA VISTA DEL WEBHOOK PARA WHATSAPP CLOUD API ---
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def webhook_whatsapp(request):
    """
    Maneja la verificación inicial de Meta (GET) y procesa los mensajes entrantes (POST).
    """
    # 1. VERIFICACIÓN DEL WEBHOOK (Petición GET)
    if request.method == 'GET':
        verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
        
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == verify_token:
            # Requisito de Meta: Retornar el challenge en texto plano con un status 200
            return HttpResponse(challenge, content_type="text/plain", status=200)
        else:
            return Response({'error': 'Token de verificación incorrecto'}, status=403)

    # 2. RECEPCIÓN DE MENSAJES (Petición POST)
    elif request.method == 'POST':
        data = request.data

        print("\n=== NUEVO MENSAJE DE WHATSAPP ===", flush=True)
        print(data, flush=True)
        print("=================================\n", flush=True)

        try:
            # Desestructuración del JSON estándar enviado por Meta
            entries = data.get('entry', [])
            if entries:
                changes = entries[0].get('changes', [])
                if changes:
                    value = changes[0].get('value', {})
                    messages = value.get('messages', [])
                    
                    if messages:
                        mensaje_info = messages[0]
                        tipo_mensaje = mensaje_info.get('type')
                        numero_remitente = mensaje_info['from']

                        logger.info('Webhook WA: tipo=%s de=%s', tipo_mensaje, numero_remitente)

                        # --- BOTÓN DE COTIZACIÓN (plantilla quick reply → type: 'button') ---
                        if tipo_mensaje == 'button':
                            payload = mensaje_info.get('button', {}).get('payload', '')
                            logger.info('Webhook WA button payload: %s', payload)
                            try:
                                accion, cotizacion_id_str = payload.split('_', 1)
                                cotizacion_obj = Cotizacion.objects.get(id=int(cotizacion_id_str))
                                if cotizacion_obj.estado == 'pendiente' and accion in ['aprobar', 'rechazar']:
                                    respuesta = 'aprobada' if accion == 'aprobar' else 'rechazada'
                                    cotizacion_obj.estado = respuesta
                                    cotizacion_obj.save()
                                    emoji = '✅' if respuesta == 'aprobada' else '❌'
                                    accion_texto = 'aprobó' if respuesta == 'aprobada' else 'rechazó'
                                    EventoMuro.objects.create(
                                        orden=cotizacion_obj.orden,
                                        tipo='nota',
                                        contenido_texto=f'{emoji} Cliente {accion_texto} la cotización vía WhatsApp.'
                                    )
                                    logger.info('Webhook WA: cotización %s → %s', cotizacion_obj.id, respuesta)
                                else:
                                    logger.warning('Webhook WA: cotización %s ya respondida o acción inválida (%s)', cotizacion_id_str, accion)
                            except (ValueError, AttributeError) as e:
                                logger.error('Webhook WA: error parseando payload "%s": %s', payload, e)
                            except Cotizacion.DoesNotExist:
                                logger.error('Webhook WA: cotización id=%s no existe', cotizacion_id_str)

                        # --- BOTÓN INTERACTIVO (respuestas de lista u otros botones no plantilla) ---
                        elif tipo_mensaje == 'interactive':
                            interactive = mensaje_info.get('interactive', {})
                            if interactive.get('type') == 'button_reply':
                                payload = interactive['button_reply'].get('id', '')
                                logger.info('Webhook WA interactive payload: %s', payload)
                                try:
                                    accion, cotizacion_id_str = payload.split('_', 1)
                                    cotizacion_obj = Cotizacion.objects.get(id=int(cotizacion_id_str))
                                    if cotizacion_obj.estado == 'pendiente' and accion in ['aprobar', 'rechazar']:
                                        respuesta = 'aprobada' if accion == 'aprobar' else 'rechazada'
                                        cotizacion_obj.estado = respuesta
                                        cotizacion_obj.save()
                                        emoji = '✅' if respuesta == 'aprobada' else '❌'
                                        accion_texto = 'aprobó' if respuesta == 'aprobada' else 'rechazó'
                                        EventoMuro.objects.create(
                                            orden=cotizacion_obj.orden,
                                            tipo='nota',
                                            contenido_texto=f'{emoji} Cliente {accion_texto} la cotización vía WhatsApp.'
                                        )
                                        logger.info('Webhook WA: cotización %s → %s', cotizacion_obj.id, respuesta)
                                except (ValueError, AttributeError) as e:
                                    logger.error('Webhook WA: error parseando interactive payload "%s": %s', payload, e)
                                except Cotizacion.DoesNotExist:
                                    logger.error('Webhook WA: cotización id=%s no existe', cotizacion_id_str)

                        # --- MENSAJE DE TEXTO LIBRE ---
                        elif tipo_mensaje == 'text':
                            texto_mensaje = mensaje_info['text']['body']
                            try:
                                cliente = Cliente.objects.get(celular=numero_remitente)
                                orden = OrdenTrabajo.objects.filter(
                                    moto__propietario=cliente,
                                    estado__in=['taller', 'lista']
                                ).order_by('-fecha_ingreso').first()
                                if orden:
                                    EventoMuro.objects.create(
                                        orden=orden,
                                        tipo='nota',
                                        contenido_texto=f"💬 Mensaje del Cliente: {texto_mensaje}"
                                    )
                            except Cliente.DoesNotExist:
                                pass
                                
        except Exception as e:
            # Mantenemos el log interno en caso de errores en la lectura de la estructura del objeto
            print(f"Error interno procesando webhook: {str(e)}")

        # Respondemos de inmediato con 200 OK a Meta para evitar reintentos duplicados por timeout
        return Response({'status': 'ok'}, status=200)
    

@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
def crear_cotizacion(request):
    orden_id = request.data.get('orden_id')
    items_raw = request.data.get('items', '[]')
    contexto = request.data.get('contexto', '').strip()
    foto = request.FILES.get('foto_evidencia')

    if isinstance(items_raw, str):
        try:
            items_data = json_module.loads(items_raw)
        except ValueError:
            return Response({'error': 'Formato de items inválido'}, status=400)
    else:
        items_data = items_raw

    if not orden_id or not items_data or not contexto:
        return Response({'error': 'Se requiere orden_id, contexto e items'}, status=400)

    try:
        orden = OrdenTrabajo.objects.get(id=orden_id)

        cotizacion = Cotizacion.objects.create(orden=orden, contexto=contexto)

        if foto:
            cotizacion.foto_evidencia = foto
            cotizacion.save()
            evento_foto = EventoMuro(orden=orden, tipo='foto')
            evento_foto.archivo.name = cotizacion.foto_evidencia.name
            evento_foto.save()

        total = 0
        for item in items_data:
            precio = float(item.get('precio', 0))
            ItemCotizacion.objects.create(
                cotizacion=cotizacion,
                descripcion=item['descripcion'],
                precio=precio
            )
            total += precio

        orden.total_cobro = total
        orden.save()

        ws = WhatsAppService()
        cliente = orden.moto.propietario
        ws.enviar_cotizacion(
            numero_cliente=cliente.celular,
            nombre_cliente=cliente.nombre,
            placa_moto=orden.moto.placa,
            total=total,
            contexto=contexto,
            cotizacion_id=cotizacion.id,
        )

        EventoMuro.objects.create(
            orden=orden,
            tipo='nota',
            contenido_texto=f'💰 Cotización enviada al cliente por ${total:.2f}: {contexto}'
        )

        return Response({'status': 'success', 'cotizacion': CotizacionSerializer(cotizacion).data})
    except OrdenTrabajo.DoesNotExist:
        return Response({'error': 'Orden no encontrada'}, status=404)
    except Exception as e:
        logger.error('crear_cotizacion: %s', e)
        return Response({'error': 'Error al crear la cotización'}, status=500)


@api_view(['GET'])
def obtener_cotizacion(request, orden_id):
    try:
        cotizaciones = Cotizacion.objects.filter(orden_id=orden_id).prefetch_related('items')
        return Response(CotizacionSerializer(cotizaciones, many=True).data)
    except Exception as e:
        logger.error('obtener_cotizacion: %s', e)
        return Response({'error': 'Error al obtener la cotización'}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def responder_cotizacion(request, cotizacion_id):
    respuesta = request.data.get('respuesta')

    if respuesta not in ['aprobada', 'rechazada']:
        return Response({'error': 'Respuesta inválida'}, status=400)

    try:
        cotizacion = Cotizacion.objects.get(id=cotizacion_id)

        if cotizacion.estado != 'pendiente':
            return Response({'error': 'Esta cotización ya fue respondida'}, status=400)

        cotizacion.estado = respuesta
        cotizacion.save()

        emoji = '✅' if respuesta == 'aprobada' else '❌'
        accion = 'aprobó' if respuesta == 'aprobada' else 'rechazó'
        EventoMuro.objects.create(
            orden=cotizacion.orden,
            tipo='nota',
            contenido_texto=f'{emoji} Cliente {accion} la cotización.'
        )

        return Response({'status': 'success', 'estado': respuesta})
    except Cotizacion.DoesNotExist:
        return Response({'error': 'Cotización no encontrada'}, status=404)
    except Exception as e:
        logger.error('responder_cotizacion: %s', e)
        return Response({'error': 'Error al procesar la respuesta'}, status=500)


@api_view(['POST'])
def entregar_orden(request):
    """
    Marca la orden como 'entregada' (la archiva) y la saca del tablero principal.
    """
    orden_id = request.data.get('orden_id')
    if not orden_id:
        return Response({'error': 'Falta el ID de la orden'}, status=400)

    try:
        # 1. Buscamos la orden
        orden = OrdenTrabajo.objects.get(id=orden_id)
        
        # 2. Cambiamos el estado a entregada (archivada)
        orden.estado = 'entregada'
        orden.fecha_entrega = timezone.now()
        total = request.data.get('total_cobro')
        if total is not None:
            orden.total_cobro = total
        orden.save()

        # 3. (Opcional pero recomendado) Dejamos registro en el muro
        EventoMuro.objects.create(
            orden=orden,
            tipo='tarea',
            contenido_texto='🏍️ Motocicleta entregada al propietario. Orden archivada.'
        )

        return Response({
            'status': 'success', 
            'mensaje': 'Orden archivada y motocicleta entregada.'
        })
    except OrdenTrabajo.DoesNotExist:
        return Response({'error': 'Orden no encontrada'}, status=404)
    except Exception as e:
        logger.error('entregar_orden: %s', e)
        return Response({'error': 'Error al entregar la orden'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historial_taller(request):
    q = request.query_params.get('q', '').strip()
    qs = OrdenTrabajo.objects.filter(estado='entregada').select_related('moto__propietario')

    if q:
        qs = qs.filter(
            Q(moto__placa__icontains=q) |
            Q(moto__propietario__nombre__icontains=q)
        )

    qs = qs.order_by('-fecha_entrega', '-fecha_ingreso')
    from .serializers import OrdenTrabajoSerializer
    return Response(OrdenTrabajoSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metricas_taller(request):
    ahora = timezone.now()
    inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    dias_umbral = int(request.query_params.get('dias', 3))
    corte_estancada = ahora - timezone.timedelta(days=dias_umbral)

    motos_activas = OrdenTrabajo.objects.filter(estado__in=['taller', 'lista']).count()

    facturado_mes = OrdenTrabajo.objects.filter(
        estado='entregada',
        fecha_entrega__gte=inicio_mes,
    ).aggregate(total=Sum('total_cobro'))['total'] or 0

    ingresos_mes = OrdenTrabajo.objects.filter(fecha_ingreso__gte=inicio_mes).count()

    estancadas_qs = OrdenTrabajo.objects.filter(
        estado='taller',
        fecha_ingreso__lte=corte_estancada,
    ).select_related('moto__propietario')

    detalle_estancadas = [
        {
            'id': o.id,
            'placa': o.moto.placa,
            'modelo': o.moto.modelo,
            'cliente': o.moto.propietario.nombre,
            'dias': (ahora - o.fecha_ingreso).days,
        }
        for o in estancadas_qs.order_by('fecha_ingreso')
    ]

    return Response({
        'motos_activas': motos_activas,
        'facturado_mes': float(facturado_mes),
        'ordenes_estancadas': len(detalle_estancadas),
        'ingresos_mes': ingresos_mes,
        'detalle_estancadas': detalle_estancadas,
        'dias_umbral': dias_umbral,
    })