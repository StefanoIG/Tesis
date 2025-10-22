from django.urls import path
from apps.usuarios import views

app_name = 'usuarios'

urlpatterns = [
    # Empresas
    path('empresas/', views.EmpresasListView.as_view(), name='empresas-list'),
    path('empresas/<uuid:pk>/', views.EmpresasDetailView.as_view(), name='empresas-detail'),
    
    # Fincas
    path('fincas/', views.FincasListView.as_view(), name='fincas-list'),
    path('fincas/<uuid:pk>/', views.FincasDetailView.as_view(), name='fincas-detail'),
    path('empresas/<uuid:empresa_id>/fincas/', views.FincasPorEmpresaView.as_view(), name='fincas-por-empresa'),
    
    # Usuarios-Empresas
    path('usuarios-empresas/', views.UsuariosEmpresasListView.as_view(), name='usuarios-empresas-list'),
    path('usuarios-empresas/<uuid:pk>/', views.UsuariosEmpresasDetailView.as_view(), name='usuarios-empresas-detail'),
    
    # Permisos
    path('permisos/', views.PermisosListView.as_view(), name='permisos-list'),
    path('permisos/<int:pk>/', views.PermisosDetailView.as_view(), name='permisos-detail'),
]
