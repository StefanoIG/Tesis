from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DispositivosSensoresViewSet, LecturasSensoresViewSet,
    ConfiguracionesAlertasSensorViewSet, RegistrosMantenimientoSensorViewSet
)

router = DefaultRouter()
router.register(r'dispositivos', DispositivosSensoresViewSet, basename='dispositivo')
router.register(r'lecturas', LecturasSensoresViewSet, basename='lectura')
router.register(r'configuraciones-alertas', ConfiguracionesAlertasSensorViewSet, basename='configuracion-alerta')
router.register(r'mantenimientos', RegistrosMantenimientoSensorViewSet, basename='mantenimiento')

urlpatterns = [
    path('', include(router.urls)),
]
