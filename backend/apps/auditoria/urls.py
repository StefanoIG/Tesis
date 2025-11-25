from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditoriasViewSet, SesionesUsuarioViewSet

router = DefaultRouter()
router.register(r'auditorias', AuditoriasViewSet, basename='auditoria')
router.register(r'sesiones', SesionesUsuarioViewSet, basename='sesion')

urlpatterns = [
    path('', include(router.urls)),
]
