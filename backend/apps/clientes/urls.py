from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientesViewSet, VentasViewSet, DetallesVentaViewSet,
    CotizacionesViewSet, HistorialInteraccionesClienteViewSet
)

router = DefaultRouter()
router.register(r'clientes', ClientesViewSet, basename='cliente')
router.register(r'ventas', VentasViewSet, basename='venta')
router.register(r'detalles-venta', DetallesVentaViewSet, basename='detalle-venta')
router.register(r'cotizaciones', CotizacionesViewSet, basename='cotizacion')
router.register(r'interacciones', HistorialInteraccionesClienteViewSet, basename='interaccion')

urlpatterns = [
    path('', include(router.urls)),
]
