from django.urls import path
from apps.procesamiento import views

app_name = 'procesamiento'

urlpatterns = [
    # Procesos
    path('procesos/', views.ProcesosProcesimientoListView.as_view(), name='procesos-list'),
    path('procesos/<uuid:pk>/', views.ProcesosProcesimientoDetailView.as_view(), name='procesos-detail'),
    
    # Inspecciones
    path('inspecciones/', views.InspeccionesCalidadListView.as_view(), name='inspecciones-list'),
    path('inspecciones/<uuid:pk>/', views.InspeccionesCalidadDetailView.as_view(), name='inspecciones-detail'),
    
    # Certificaciones
    path('certificaciones/', views.CertificacionesEstandaresListView.as_view(), name='certificaciones-list'),
    path('certificaciones/<uuid:pk>/', views.CertificacionesEstandaresDetailView.as_view(), name='certificaciones-detail'),
    
    # Análisis de laboratorio
    path('analisis-laboratorio/', views.ResultadosAnalisisListView.as_view(), name='analisis-list'),
    path('analisis-laboratorio/<uuid:pk>/', views.ResultadosAnalisisDetailView.as_view(), name='analisis-detail'),
]
