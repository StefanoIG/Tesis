from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.usuarios.models import Empresas, Fincas, UsuariosEmpresas, Permisos, RolesPermisos
from apps.usuarios.serializers import (
    EmpresasSerializer, FincasSerializer, UsuariosEmpresasSerializer, PermisosSerializer
)


# Empresas
class EmpresasListView(generics.ListCreateAPIView):
    """Listar y crear empresas"""
    queryset = Empresas.objects.all()
    serializer_class = EmpresasSerializer
    permission_classes = [IsAuthenticated]


class EmpresasDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar empresa"""
    queryset = Empresas.objects.all()
    serializer_class = EmpresasSerializer
    permission_classes = [IsAuthenticated]


# Fincas
class FincasListView(generics.ListCreateAPIView):
    """Listar y crear fincas"""
    queryset = Fincas.objects.all()
    serializer_class = FincasSerializer
    permission_classes = [IsAuthenticated]


class FincasDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar finca"""
    queryset = Fincas.objects.all()
    serializer_class = FincasSerializer
    permission_classes = [IsAuthenticated]


# Usuarios-Empresas
class UsuariosEmpresasListView(generics.ListCreateAPIView):
    """Listar y crear relaciones usuario-empresa"""
    queryset = UsuariosEmpresas.objects.all()
    serializer_class = UsuariosEmpresasSerializer
    permission_classes = [IsAuthenticated]


class UsuariosEmpresasDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar relación usuario-empresa"""
    queryset = UsuariosEmpresas.objects.all()
    serializer_class = UsuariosEmpresasSerializer
    permission_classes = [IsAuthenticated]


# Permisos
class PermisosListView(generics.ListAPIView):
    """Listar permisos"""
    queryset = Permisos.objects.all()
    serializer_class = PermisosSerializer
    permission_classes = [IsAuthenticated]


class PermisosDetailView(generics.RetrieveAPIView):
    """Obtener permiso"""
    queryset = Permisos.objects.all()
    serializer_class = PermisosSerializer
    permission_classes = [IsAuthenticated]


# Fincas por Empresa
class FincasPorEmpresaView(generics.ListAPIView):
    """Listar fincas de una empresa específica"""
    serializer_class = FincasSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        empresa_id = self.kwargs['empresa_id']
        return Fincas.objects.filter(empresa_id=empresa_id)
