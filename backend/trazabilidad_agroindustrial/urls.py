from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 endpoints
    path('api/v1/auth/', include('apps.autenticacion.urls')),
    path('api/v1/usuarios/', include('apps.usuarios.urls')),
    path('api/v1/trazabilidad/', include('apps.trazabilidad.urls')),
    path('api/v1/procesamiento/', include('apps.procesamiento.urls')),
    path('api/v1/logistica/', include('apps.logistica.urls')),
    path('api/v1/reportes/', include('apps.reportes.urls')),
    path('api/v1/documentos/', include('apps.documentos.urls')),
    path('api/v1/sincronizacion/', include('apps.sincronizacion.urls')),
    path('api/v1/administracion/', include('apps.administracion.urls')),
    path('api/v1/alertas/', include('apps.alertas.urls')),
    path('api/v1/notificaciones/', include('apps.notificaciones.urls')),
    
    # Nuevas apps
    path('api/v1/auditoria/', include('apps.auditoria.urls')),
    path('api/v1/roles-permisos/', include('apps.roles_permisos.urls')),
    path('api/v1/certificaciones/', include('apps.certificaciones.urls')),
    path('api/v1/sensores/', include('apps.sensores.urls')),
    path('api/v1/clientes/', include('apps.clientes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
