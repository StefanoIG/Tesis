from django.urls import path
from apps.alertas import views

app_name = 'alertas'

urlpatterns = [
    # Reglas
    path('reglas/', views.ReglasAlertasListView.as_view(), name='reglas-list'),
    path('reglas/<uuid:pk>/', views.ReglasAlertasDetailView.as_view(), name='reglas-detail'),
    
    # Alertas
    path('alertas/', views.AlertasListView.as_view(), name='alertas-list'),
    path('alertas/<uuid:pk>/', views.AlertasDetailView.as_view(), name='alertas-detail'),
    path('alertas/<uuid:pk>/resolver/', views.AlertasResolverView.as_view(), name='alertas-resolver'),
    path('alertas/abiertas/', views.AlertasAbiertasView.as_view(), name='alertas-abiertas'),
]
