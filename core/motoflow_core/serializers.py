from rest_framework import serializers
from .models import Cliente, Motocicleta, OrdenTrabajo, EventoMuro, Cotizacion, ItemCotizacion

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class MotocicletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motocicleta
        fields = '__all__'

class OrdenTrabajoSerializer(serializers.ModelSerializer):
    placa_moto = serializers.CharField(source='moto.placa', read_only=True)
    modelo_moto = serializers.CharField(source='moto.modelo', read_only=True)
    nombre_cliente = serializers.CharField(source='moto.propietario.nombre', read_only=True)
    celular_cliente = serializers.CharField(source='moto.propietario.celular', read_only=True)

    class Meta:
        model = OrdenTrabajo
        fields = '__all__'

class EventoMuroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoMuro
        fields = '__all__'

class ItemCotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCotizacion
        fields = ['id', 'descripcion', 'precio']

class CotizacionSerializer(serializers.ModelSerializer):
    items = ItemCotizacionSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cotizacion
        fields = ['id', 'estado', 'contexto', 'foto_evidencia', 'fecha_envio', 'items', 'total']

    def get_total(self, obj):
        return float(sum(item.precio for item in obj.items.all()))

class EventoMuroBasicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoMuro
        # CORRECCIÓN: Agregamos 'contenido_texto' y 'fecha' para que el cliente pueda leer las tareas
        fields = ['id', 'tipo', 'contenido_texto', 'archivo', 'completada', 'fecha'] 

class SeguimientoOrdenSerializer(serializers.ModelSerializer):
    eventos = serializers.SerializerMethodField()
    cotizacion = serializers.SerializerMethodField()
    placa_moto = serializers.CharField(source='moto.placa', read_only=True)
    modelo_moto = serializers.CharField(source='moto.modelo', read_only=True)
    nombre_cliente = serializers.CharField(source='moto.propietario.nombre', read_only=True)

    class Meta:
        model = OrdenTrabajo
        fields = [
            'id', 'hash_seguimiento', 'estado', 'total_cobro', 'fecha_ingreso',
            'placa_moto', 'modelo_moto', 'nombre_cliente', 'eventos', 'cotizacion'
        ]

    def get_eventos(self, obj):
        eventos_de_la_orden = EventoMuro.objects.filter(orden=obj).order_by('id')
        return EventoMuroBasicoSerializer(eventos_de_la_orden, many=True).data

    def get_cotizacion(self, obj):
        cotizaciones = obj.cotizaciones.prefetch_related('items').all()
        return CotizacionSerializer(cotizaciones, many=True).data