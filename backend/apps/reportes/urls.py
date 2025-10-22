from django.urls import path
from apps.reportes import views

app_name = 'reportes'

urlpatterns = [
    # Reportes
    path('reportes/', views.ReportesListView.as_view(), name='reportes-list'),
    path('reportes/<uuid:pk>/', views.ReportesDetailView.as_view(), name='reportes-detail'),
    path('reportes/<uuid:pk>/descargar/', views.ReportesDescargarView.as_view(), name='reportes-descargar'),
    path('reportes/generar/trazabilidad/', views.GenerarReporteTrazabilidadView.as_view(), name='generar-trazabilidad'),
    
    # KPIs
    path('kpis/', views.IndicesKPIListView.as_view(), name='kpis-list'),
    path('kpis/<uuid:pk>/', views.IndicesKPIDetailView.as_view(), name='kpis-detail'),
    
    # Dashboards
    path('dashboards/mi-dashboard/', views.MiDashboardView.as_view(), name='mi-dashboard'),
    path('dashboards/', views.DashboardDatosListView.as_view(), name='dashboards-list'),
    path('dashboards/<uuid:pk>/', views.DashboardDatosDetailView.as_view(), name='dashboards-detail'),
]
