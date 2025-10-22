from rest_framework import serializers
from apps.usuarios.models import Empresas, Fincas, UsuariosEmpresas, Permisos, RolesPermisos


class EmpresasSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Empresas"""
    class Meta:
        model = Empresas
        fields = [
            'id', 'nombre', 'tipo_empresa', 'registro_nacional', 'email',
            'telefono', 'direccion', 'ciudad', 'pais', 'es_activa',
            'certificaciones', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en', 'nombre', 'tipo_empresa']


class FincasSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Fincas"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

    class Meta:
        model = Fincas
        fields = [
            'id', 'empresa', 'empresa_nombre', 'nombre', 'codigo_finca',
            'direccion', 'ciudad', 'coordenadas_latitud', 'coordenadas_longitud',
            'tamaño_hectareas', 'es_activa', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


class PermisosSerializer(serializers.ModelSerializer):
    """Serializer para Permisos"""
    class Meta:
        model = Permisos
        fields = ['id', 'nombre', 'descripcion', 'codigo']
        read_only_fields = ['id']


class RolesPermisosSerializer(serializers.ModelSerializer):
    """Serializer para RolesPermisos"""
    permiso_detalle = PermisosSerializer(source='permiso', read_only=True)

    class Meta:
        model = RolesPermisos
        fields = ['id', 'rol', 'permiso', 'permiso_detalle']
        read_only_fields = ['id']


class UsuariosEmpresasSerializer(serializers.ModelSerializer):
    """Serializer para UsuariosEmpresas"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    finca_nombre = serializers.CharField(source='finca.nombre', read_only=True, allow_null=True)

    class Meta:
        model = UsuariosEmpresas
        fields = [
            'id', 'usuario', 'usuario_email', 'empresa', 'empresa_nombre',
            'finca', 'finca_nombre', 'es_responsable', 'fecha_asignacion'
        ]
        read_only_fields = ['id', 'fecha_asignacion']
