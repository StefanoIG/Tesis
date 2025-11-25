from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CertificacionesViewSet, CertificacionesProductoresViewSet,
    CertificacionesLotesViewSet, RequisitosCumplimientoViewSet,
    CumplimientoNormativoViewSet
)

router = DefaultRouter()
router.register(r'certificaciones', CertificacionesViewSet, basename='certificacion')
router.register(r'certificaciones-productores', CertificacionesProductoresViewSet, basename='certificacion-productor')
router.register(r'certificaciones-lotes', CertificacionesLotesViewSet, basename='certificacion-lote')
router.register(r'requisitos', RequisitosCumplimientoViewSet, basename='requisito')
router.register(r'cumplimientos', CumplimientoNormativoViewSet, basename='cumplimiento')

urlpatterns = [
    path('', include(router.urls)),
]
