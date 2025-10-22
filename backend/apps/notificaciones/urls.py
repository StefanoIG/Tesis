from django.urls import path
from apps.notificaciones import views

app_name = 'notificaciones'

urlpatterns = [
    # Notificaciones (Polling)
    path('notificaciones/no-leidas/', views.NotificacionesNoLeidasView.as_view(), name='notificaciones-no-leidas'),
    path('notificaciones/', views.NotificacionesListView.as_view(), name='notificaciones-list'),
    path('notificaciones/<uuid:pk>/', views.NotificacionesDetailView.as_view(), name='notificaciones-detail'),
    path('notificaciones/<uuid:pk>/marcar-leida/', views.MarcarLeidaView.as_view(), name='marcar-leida'),
    path('notificaciones/marcar-todas-leidas/', views.MarcarTodasLeidasView.as_view(), name='marcar-todas-leidas'),
    
    # Preferencias
    path('preferencias/', views.PreferenciasView.as_view(), name='preferencias-detail'),
    
    # Historial
    path('historial-lectura/', views.HistorialLecturaListView.as_view(), name='historial-lectura-list'),
]
