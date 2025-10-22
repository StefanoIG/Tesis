from django.urls import path
from apps.documentos import views

app_name = 'documentos'

urlpatterns = [
    # Documentos
    path('documentos/', views.DocumentosListView.as_view(), name='documentos-list'),
    path('documentos/<uuid:pk>/', views.DocumentosDetailView.as_view(), name='documentos-detail'),
    path('documentos/<uuid:pk>/validar/', views.DocumentosValidarView.as_view(), name='documentos-validar'),
    path('documentos/<uuid:pk>/descargar/', views.DocumentosDescargarView.as_view(), name='documentos-descargar'),
    
    # Fotos
    path('fotos/', views.FotosProductosListView.as_view(), name='fotos-list'),
    path('fotos/<uuid:pk>/', views.FotosProductosDetailView.as_view(), name='fotos-detail'),
]
