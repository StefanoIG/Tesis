from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.autenticacion import views

app_name = 'autenticacion'

urlpatterns = [
    # Token JWT
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registro e inicio de sesión
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Usuarios
    path('usuarios/', views.UsuariosListView.as_view(), name='usuarios-list'),
    path('usuarios/<uuid:pk>/', views.UsuariosDetailView.as_view(), name='usuarios-detail'),
    
    # Roles
    path('roles/', views.RolesListView.as_view(), name='roles-list'),
    path('roles/<int:pk>/', views.RolesDetailView.as_view(), name='roles-detail'),
    
    # Auditoría
    path('auditorias/', views.AuditoriasListView.as_view(), name='auditorias-list'),
    path('auditorias/<uuid:pk>/', views.AuditoriasDetailView.as_view(), name='auditorias-detail'),
]
