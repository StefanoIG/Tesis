from rest_framework import serializers
from .models import Roles, Permisos, RolesPermisos, UsuariosRoles, PermisosEspeciales


class PermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permisos
        fields = [
            'id', 'nombre_permiso', 'codigo_permiso', 'descripcion',
            'tipo_permiso', 'modulo', 'recurso',
            'es_activo', 'es_critico',
            'creado_en', 'actualizado_en'
        ]


class RolesPermisosSerializer(serializers.ModelSerializer):
    permiso_detalle = PermisosSerializer(source='permiso', read_only=True)

    class Meta:
        model = RolesPermisos
        fields = ['id', 'rol', 'permiso', 'permiso_detalle', 'fecha_asignacion']


class RolesSerializer(serializers.ModelSerializer):
    permisos = serializers.SerializerMethodField()
    cantidad_usuarios = serializers.SerializerMethodField()

    class Meta:
        model = Roles
        fields = [
            'id', 'nombre_rol', 'codigo_rol', 'descripcion',
            'tipo_rol', 'es_activo', 'nivel_acceso',
            'permisos', 'cantidad_usuarios',
            'creado_en', 'actualizado_en'
        ]

    def get_permisos(self, obj):
        permisos_rel = RolesPermisos.objects.filter(rol=obj).select_related('permiso')
        return PermisosSerializer([rp.permiso for rp in permisos_rel], many=True).data

    def get_cantidad_usuarios(self, obj):
        return UsuariosRoles.objects.filter(rol=obj, es_activo=True).count()


class UsuariosRolesSerializer(serializers.ModelSerializer):
    rol_detalle = RolesSerializer(source='rol', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    finca_nombre = serializers.CharField(source='finca.nombre', read_only=True)

    class Meta:
        model = UsuariosRoles
        fields = [
            'id', 'usuario', 'usuario_email', 'usuario_nombre',
            'rol', 'rol_detalle',
            'empresa', 'empresa_nombre',
            'finca', 'finca_nombre',
            'es_activo', 'fecha_inicio', 'fecha_fin',
            'asignado_por', 'motivo'
        ]


class PermisosEspecialesSerializer(serializers.ModelSerializer):
    permiso_detalle = PermisosSerializer(source='permiso', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

    class Meta:
        model = PermisosEspeciales
        fields = [
            'id', 'usuario', 'usuario_email',
            'permiso', 'permiso_detalle',
            'tipo', 'empresa', 'empresa_nombre',
            'es_activo', 'fecha_inicio', 'fecha_fin',
            'concedido_por', 'motivo'
        ]
