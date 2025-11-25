from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstudiosSueloViewSet, ParcelasViewSet, CatalogosCultivosViewSet,
    PlanesCultivoViewSet, CalendariosRiegoViewSet, RegistrosRiegoViewSet,
    PermisosNacionalesEcuadorViewSet, PermisosObtenidosViewSet
)

router = DefaultRouter()
router.register(r'estudios-suelo', EstudiosSueloViewSet, basename='estudios-suelo')
router.register(r'parcelas', ParcelasViewSet, basename='parcelas')
router.register(r'catalogos-cultivos', CatalogosCultivosViewSet, basename='catalogos-cultivos')
router.register(r'planes-cultivo', PlanesCultivoViewSet, basename='planes-cultivo')
router.register(r'calendarios-riego', CalendariosRiegoViewSet, basename='calendarios-riego')
router.register(r'registros-riego', RegistrosRiegoViewSet, basename='registros-riego')
router.register(r'permisos-nacionales', PermisosNacionalesEcuadorViewSet, basename='permisos-nacionales')
router.register(r'permisos-obtenidos', PermisosObtenidosViewSet, basename='permisos-obtenidos')

urlpatterns = [
    path('', include(router.urls)),
]
