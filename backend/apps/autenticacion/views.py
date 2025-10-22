from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.autenticacion.models import Usuarios, Roles, UsuariosRoles, Auditorias
from apps.autenticacion.serializers import (
    UsuarioSerializer, RolSerializer, CustomTokenObtainPairSerializer,
    AuditoriaSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Obtener token JWT con información del usuario"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegistroView(generics.CreateAPIView):
    """Registrar nuevo usuario"""
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    """Cerrar sesión"""
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer
    
    def post(self, request, *args, **kwargs):
        return Response(
            {'mensaje': 'Sesión cerrada exitosamente'},
            status=status.HTTP_200_OK
        )


class UsuariosListView(generics.ListCreateAPIView):
    """Listar y crear usuarios"""
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]


class UsuariosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar usuario"""
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]


class RolesListView(generics.ListCreateAPIView):
    """Listar y crear roles"""
    queryset = Roles.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]


class RolesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar rol"""
    queryset = Roles.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]


class AuditoriasListView(generics.ListAPIView):
    """Listar auditorías"""
    queryset = Auditorias.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAuthenticated]


class AuditoriasDetailView(generics.RetrieveAPIView):
    """Obtener auditoría"""
    queryset = Auditorias.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAuthenticated]
