from django.urls import path
from apps.administracion import views

app_name = 'administracion'

urlpatterns = [
    # Configuración
    path('configuracion/', views.ConfiguracionSistemaView.as_view(), name='configuracion-detail'),
    
    # Logs
    path('logs-acceso/', views.LogsAccesoListView.as_view(), name='logs-acceso-list'),
    path('logs-acceso/<uuid:pk>/', views.LogsAccesoDetailView.as_view(), name='logs-acceso-detail'),
    
    path('logs-actividad/', views.LogsActividadListView.as_view(), name='logs-actividad-list'),
    path('logs-actividad/<uuid:pk>/', views.LogsActividadDetailView.as_view(), name='logs-actividad-detail'),
    
    # Backups
    path('backups/', views.BackupsSistemaListView.as_view(), name='backups-list'),
    path('backups/<uuid:pk>/', views.BackupsSistemaDetailView.as_view(), name='backups-detail'),
    path('backups/ejecutar/', views.EjecutarBackupView.as_view(), name='backups-ejecutar'),
]
