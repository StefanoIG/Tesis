from django.urls import path
from apps.trazabilidad import views

app_name = 'trazabilidad'

urlpatterns = [
    # Productos
    path('productos/', views.ProductosListView.as_view(), name='productos-list'),
    path('productos/<uuid:pk>/', views.ProductosDetailView.as_view(), name='productos-detail'),
    
    # Lotes
    path('lotes/', views.LotesListView.as_view(), name='lotes-list'),
    path('lotes/<uuid:pk>/', views.LotesDetailView.as_view(), name='lotes-detail'),
    path('lotes/<uuid:pk>/eventos/', views.LotesEventosView.as_view(), name='lotes-eventos'),
    path('lotes/<uuid:pk>/historial/', views.LotesHistorialView.as_view(), name='lotes-historial'),
    path('lotes/<uuid:pk>/generar-qr/', views.LotesGenerarQRView.as_view(), name='lotes-generar-qr'),
    
    # Tipos de eventos
    path('tipos-eventos/', views.TiposEventosListView.as_view(), name='tipos-eventos-list'),
    path('tipos-eventos/<int:pk>/', views.TiposEventosDetailView.as_view(), name='tipos-eventos-detail'),
    
    # Eventos de trazabilidad
    path('eventos/', views.EventosListView.as_view(), name='eventos-list'),
    path('eventos/<uuid:pk>/', views.EventosDetailView.as_view(), name='eventos-detail'),
]
