from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RolesViewSet, PermisosViewSet, UsuariosRolesViewSet,
    PermisosEspecialesViewSet
)

router = DefaultRouter()
router.register(r'roles', RolesViewSet, basename='rol')
router.register(r'permisos', PermisosViewSet, basename='permiso')
router.register(r'usuarios-roles', UsuariosRolesViewSet, basename='usuario-rol')
router.register(r'permisos-especiales', PermisosEspecialesViewSet, basename='permiso-especial')

urlpatterns = [
    path('', include(router.urls)),
]
