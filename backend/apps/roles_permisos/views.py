from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Roles, Permisos, RolesPermisos, UsuariosRoles, PermisosEspeciales
from .serializers import (
    RolesSerializer, PermisosSerializer, RolesPermisosSerializer,
    UsuariosRolesSerializer, PermisosEspecialesSerializer
)


class RolesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de roles.
    """
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['es_activo', 'tipo_rol', 'nivel_acceso']
    search_fields = ['nombre_rol', 'codigo_rol', 'descripcion']
    ordering_fields = ['nombre_rol', 'nivel_acceso', 'creado_en']
    ordering = ['-nivel_acceso']

    @action(detail=True, methods=['post'])
    def asignar_permiso(self, request, pk=None):
        """Asigna un permiso a un rol."""
        rol = self.get_object()
        permiso_id = request.data.get('permiso_id')
        
        if not permiso_id:
            return Response(
                {'error': 'Se requiere permiso_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            permiso = Permisos.objects.get(id=permiso_id)
            rol_permiso, created = RolesPermisos.objects.get_or_create(
                rol=rol,
                permiso=permiso,
                defaults={'concedido_por': request.user}
            )
            
            if created:
                return Response(
                    {'message': 'Permiso asignado exitosamente'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'El permiso ya estaba asignado'},
                    status=status.HTTP_200_OK
                )
        except Permisos.DoesNotExist:
            return Response(
                {'error': 'Permiso no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remover_permiso(self, request, pk=None):
        """Remueve un permiso de un rol."""
        rol = self.get_object()
        permiso_id = request.data.get('permiso_id')
        
        if not permiso_id:
            return Response(
                {'error': 'Se requiere permiso_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            RolesPermisos.objects.filter(rol=rol, permiso_id=permiso_id).delete()
            return Response({'message': 'Permiso removido exitosamente'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PermisosViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de permisos.
    """
    queryset = Permisos.objects.all()
    serializer_class = PermisosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_permiso', 'modulo', 'recurso', 'es_activo', 'es_critico']
    search_fields = ['nombre_permiso', 'codigo_permiso', 'descripcion']
    ordering_fields = ['nombre_permiso', 'modulo']
    ordering = ['modulo', 'recurso']

    @action(detail=False, methods=['get'])
    def por_modulo(self, request):
        """Agrupa permisos por módulo."""
        modulos = {}
        for permiso in self.queryset.filter(es_activo=True):
            if permiso.modulo not in modulos:
                modulos[permiso.modulo] = []
            modulos[permiso.modulo].append(PermisosSerializer(permiso).data)
        
        return Response(modulos)


class UsuariosRolesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para asignación de roles a usuarios.
    """
    queryset = UsuariosRoles.objects.select_related(
        'usuario', 'rol', 'empresa', 'finca'
    ).all()
    serializer_class = UsuariosRolesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['usuario', 'rol', 'empresa', 'finca', 'es_activo']
    ordering_fields = ['fecha_inicio']
    ordering = ['-fecha_inicio']

    @action(detail=False, methods=['get'])
    def mis_roles(self, request):
        """Obtiene los roles del usuario actual."""
        roles = self.queryset.filter(
            usuario=request.user,
            es_activo=True
        )
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """Desactiva una asignación de rol."""
        asignacion = self.get_object()
        asignacion.es_activo = False
        asignacion.save()
        return Response({'message': 'Rol desactivado exitosamente'})


class PermisosEspecialesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de permisos especiales.
    """
    queryset = PermisosEspeciales.objects.select_related(
        'usuario', 'permiso', 'empresa'
    ).all()
    serializer_class = PermisosEspecialesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['usuario', 'permiso', 'tipo', 'empresa', 'es_activo']
    ordering_fields = ['fecha_inicio']
    ordering = ['-fecha_inicio']

    @action(detail=False, methods=['get'])
    def mis_permisos_especiales(self, request):
        """Obtiene los permisos especiales del usuario actual."""
        permisos = self.queryset.filter(
            usuario=request.user,
            es_activo=True
        )
        serializer = self.get_serializer(permisos, many=True)
        return Response(serializer.data)
