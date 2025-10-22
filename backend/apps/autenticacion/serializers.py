from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.autenticacion.models import Usuarios, Roles, UsuariosRoles, Auditorias
from datetime import datetime


class RolSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Roles"""
    class Meta:
        model = Roles
        fields = ['id', 'nombre_rol', 'descripcion']
        read_only_fields = ['id']


class UsuarioRolSerializer(serializers.ModelSerializer):
    """Serializer para la asignación de roles a usuarios"""
    rol_detalle = RolSerializer(source='rol', read_only=True)

    class Meta:
        model = UsuariosRoles
        fields = ['id', 'rol', 'rol_detalle', 'asignado_en']
        read_only_fields = ['id', 'asignado_en']


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer completo para Usuarios con roles anidados"""
    roles = UsuarioRolSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuarios
        fields = [
            'id', 'username', 'email', 'nombre_completo', 'password', 'password2',
            'telefono', 'activo', 'ultimo_acceso', 'roles', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en', 'ultimo_acceso']
        extra_kwargs = {
            'username': {'required': True},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        usuario = Usuarios(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UsuarioListaSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados de usuarios"""
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Usuarios
        fields = ['id', 'username', 'email', 'nombre_completo', 'telefono', 'activo', 'roles']

    def get_roles(self, obj):
        roles = obj.roles.all()
        return [{'id': r.rol.id, 'nombre': r.rol.nombre_rol} for r in roles]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para obtener tokens JWT con información adicional del usuario.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar información personalizada al token
        token['email'] = user.email
        # Usar nombre_completo si existe (modelo Usuarios), sino usar first_name
        if hasattr(user, 'nombre_completo'):
            token['nombre_completo'] = user.nombre_completo
        else:
            token['nombre_completo'] = f"{user.first_name} {user.last_name}".strip() or user.username
        
        # Agregar roles si existen
        if hasattr(user, 'roles'):
            token['roles'] = list(
                user.roles.values_list('rol__nombre_rol', flat=True)
            )
        else:
            token['roles'] = []

        token['activo'] = getattr(user, 'activo', user.is_active)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        usuario = self.user

        # Actualizar último acceso si el modelo lo soporta
        if hasattr(usuario, 'ultimo_acceso'):
            usuario.ultimo_acceso = datetime.now()
            usuario.save(update_fields=['ultimo_acceso'])

        # Agregar información del usuario a la respuesta
        nombre_completo = getattr(usuario, 'nombre_completo', None)
        if not nombre_completo:
            nombre_completo = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.username
        
        roles_list = []
        if hasattr(usuario, 'roles'):
            roles_list = list(
                usuario.roles.values_list('rol__nombre_rol', flat=True)
            )

        data['usuario'] = {
            'id': str(usuario.id),
            'email': usuario.email,
            'nombre_completo': nombre_completo,
            'roles': roles_list,
        }

        return data


class TokenRefreshSerializer(serializers.Serializer):
    """Serializer para refrescar tokens"""
    refresh = serializers.CharField()


class RegistroSerializer(serializers.ModelSerializer):
    """Serializer para el registro de nuevos usuarios"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    rol_inicial = serializers.PrimaryKeyRelatedField(
        queryset=Roles.objects.all(),
        required=True,
        write_only=True
    )

    class Meta:
        model = Usuarios
        fields = ['id', 'username', 'email', 'nombre_completo', 'telefono', 'password', 'password2', 'rol_inicial']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden."}
            )
        return attrs

    def create(self, validated_data):
        rol = validated_data.pop('rol_inicial')
        validated_data.pop('password2')
        password = validated_data.pop('password')

        usuario = Usuarios(**validated_data)
        usuario.set_password(password)
        usuario.save()

        # Asignar rol inicial
        UsuariosRoles.objects.create(usuario=usuario, rol=rol)

        return usuario


class AuditoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Auditorias"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = Auditorias
        fields = [
            'id', 'usuario', 'usuario_email', 'accion', 'entidad_afectada',
            'registro_id', 'datos_anteriores', 'datos_nuevos', 'ip_origen',
            'user_agent', 'timestamp', 'resultado', 'mensaje_error'
        ]
        read_only_fields = ['id', 'timestamp']
