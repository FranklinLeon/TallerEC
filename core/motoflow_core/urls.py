from django.contrib import admin
from django.urls import path, include
from django.conf import settings               # Para leer las variables de settings.py
from django.conf.urls.static import static     # Para generar la ruta de los archivos
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet,
    MotocicletaViewSet,
    OrdenTrabajoViewSet,
    EventoMuroViewSet,
    procesar_nota_voz,
    probar_conexion_ia,
    SeguimientoClienteView,
    escanear_placa,
    registrar_ingreso_moto,
    finalizar_orden,
    webhook_whatsapp,
    entregar_orden,
    crear_cotizacion,
    obtener_cotizacion,
    responder_cotizacion,
    metricas_taller,
    historial_taller,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Creamos el router principal
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'motos', MotocicletaViewSet)
router.register(r'ordenes', OrdenTrabajoViewSet)
router.register(r'muro', EventoMuroViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- ENDPOINTS DE AUTENTICACIÓN ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- 1. RUTAS ESPECÍFICAS PRIMERO ---
    # Colocamos las rutas manuales antes del router para que Django las evalúe primero
    path('api/webhook/whatsapp/', webhook_whatsapp, name='webhook-whatsapp'), # <-- NUEVA RUTA DEL WEBHOOK
    path('api/ping-ia/', probar_conexion_ia, name='ping-ia'),
    path('api/muro/audio/', procesar_nota_voz, name='procesar_audio'),
    
    # Nueva ruta segura para el cliente 
    path('api/seguimiento/<uuid:hash_seguimiento>/', SeguimientoClienteView.as_view(), name='seguimiento-cliente'),

    path('api/motos/escanear/', escanear_placa, name='escanear-placa'),

    path('api/motos/registrar/', registrar_ingreso_moto),

    path('api/motos/finalizar/', finalizar_orden),

    path('api/motos/entregar/', entregar_orden),

    path('api/cotizacion/crear/', crear_cotizacion, name='crear-cotizacion'),
    path('api/cotizacion/<int:orden_id>/', obtener_cotizacion, name='obtener-cotizacion'),
    path('api/cotizacion/<int:cotizacion_id>/responder/', responder_cotizacion, name='responder-cotizacion'),

    path('api/metricas/', metricas_taller, name='metricas-taller'),
    path('api/motos/historial/', historial_taller, name='historial-taller'),

    # --- 2. RUTAS DEL ROUTER DESPUÉS ---
    # El router atrapará cualquier otra cosa que vaya a /api/...
    path('api/', include(router.urls)),
]

# Configuración para servir archivos multimedia (fotos) durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)