from django.urls import path
from apps.sincronizacion import views

app_name = 'sincronizacion'

urlpatterns = [
    # Estados de sincronización
    path('estados/', views.EstadosSincronizacionListView.as_view(), name='estados-list'),
    path('estados/<uuid:pk>/', views.EstadosSincronizacionDetailView.as_view(), name='estados-detail'),
    
    # Sincronizar
    path('sincronizar/', views.SincronizarView.as_view(), name='sincronizar'),
    path('sincronizar/upload/', views.SincronizarUploadView.as_view(), name='sincronizar-upload'),
    path('sincronizar/download/', views.SincronizarDownloadView.as_view(), name='sincronizar-download'),
    
    # Conflictos
    path('conflictos/', views.ConflictosListView.as_view(), name='conflictos-list'),
    path('conflictos/<uuid:pk>/', views.ConflictosDetailView.as_view(), name='conflictos-detail'),
    path('conflictos/<uuid:pk>/resolver/', views.ConflictosResolverView.as_view(), name='conflictos-resolver'),
    
    # Registros
    path('registros/', views.RegistrosSincronizacionListView.as_view(), name='registros-list'),
    
    # Versiones
    path('versiones-db/', views.VersionesDBListView.as_view(), name='versiones-db-list'),
    path('versiones-db/<uuid:pk>/', views.VersionesDBDetailView.as_view(), name='versiones-db-detail'),
]
