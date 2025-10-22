from django.urls import path
from apps.logistica import views

app_name = 'logistica'

urlpatterns = [
    # Vehículos
    path('vehiculos/', views.VehiculosListView.as_view(), name='vehiculos-list'),
    path('vehiculos/<uuid:pk>/', views.VehiculosDetailView.as_view(), name='vehiculos-detail'),
    
    # Conductores
    path('conductores/', views.ConductoresListView.as_view(), name='conductores-list'),
    path('conductores/<uuid:pk>/', views.ConductoresDetailView.as_view(), name='conductores-detail'),
    
    # Envíos
    path('envios/', views.EnviosListView.as_view(), name='envios-list'),
    path('envios/<uuid:pk>/', views.EnviosDetailView.as_view(), name='envios-detail'),
    path('envios/<uuid:pk>/tracking/', views.EnviosTrackingView.as_view(), name='envios-tracking'),
    
    # Tracking en tiempo real
    path('tracking/', views.TrackingListView.as_view(), name='tracking-list'),
    path('tracking/<uuid:pk>/', views.TrackingDetailView.as_view(), name='tracking-detail'),
    
    # Alertas logísticas
    path('alertas/', views.AlertasLogisticaListView.as_view(), name='alertas-list'),
    path('alertas/<uuid:pk>/', views.AlertasLogisticaDetailView.as_view(), name='alertas-detail'),
]
