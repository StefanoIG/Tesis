from rest_framework import serializers
from .models import SesionesUsuario
from apps.autenticacion.models import Auditorias


class AuditoriasSerializer(serializers.ModelSerializer):
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)

    class Meta:
        model = Auditorias
        fields = [
            'id', 'usuario', 'usuario_email', 'usuario_nombre',
            'accion', 'entidad_afectada', 'registro_id',
            'datos_anteriores', 'datos_nuevos',
            'ip_origen', 'user_agent',
            'resultado', 'mensaje_error',
            'metadatos', 'timestamp'
        ]
        read_only_fields = fields


class SesionesUsuarioSerializer(serializers.ModelSerializer):
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)
    duracion_minutos = serializers.SerializerMethodField()

    class Meta:
        model = SesionesUsuario
        fields = [
            'id', 'usuario', 'usuario_email', 'usuario_nombre',
            'token_sesion', 'ip_origen', 'user_agent', 'dispositivo',
            'pais', 'ciudad',
            'fecha_inicio', 'fecha_ultima_actividad', 'fecha_cierre',
            'estado', 'duracion_minutos', 'metadatos'
        ]
        read_only_fields = fields

    def get_duracion_minutos(self, obj):
        if obj.fecha_cierre:
            delta = obj.fecha_cierre - obj.fecha_inicio
        else:
            delta = obj.fecha_ultima_actividad - obj.fecha_inicio
        return int(delta.total_seconds() / 60)
