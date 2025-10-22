from rest_framework import serializers
from apps.administracion.models import (
    ConfiguracionSistema, LogsAcceso, LogsActividad, BackupsSistema
)


class ConfiguracionSistemaSerializer(serializers.ModelSerializer):
    """Serializer para ConfiguracionSistema"""
    class Meta:
        model = ConfiguracionSistema
        fields = [
            'id', 'productos_permitidos', 'tipos_eventos_permitidos',
            'unidades_medida', 'intervalo_sincronizacion_minutos',
            'intervalo_notificaciones_minutos', 'tamaño_maximo_documento_mb',
            'dias_retencion_documentos', 'intentos_fallidos_max',
            'bloqueo_minutos', 'sesion_duracion_horas', 'actualizado_en'
        ]
        read_only_fields = ['id', 'actualizado_en']


class LogsAccesoSerializer(serializers.ModelSerializer):
    """Serializer para LogsAcceso"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True, allow_null=True)

    class Meta:
        model = LogsAcceso
        fields = [
            'id', 'usuario', 'usuario_email', 'tipo_acceso', 'ip_origen',
            'user_agent', 'motivo_fallo', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class LogsActividadSerializer(serializers.ModelSerializer):
    """Serializer para LogsActividad"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True, allow_null=True)

    class Meta:
        model = LogsActividad
        fields = [
            'id', 'usuario', 'usuario_email', 'tipo_actividad', 'modulo',
            'entidad', 'registro_id', 'descripcion', 'datos_antes',
            'datos_despues', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class BackupsSistemaSerializer(serializers.ModelSerializer):
    """Serializer para BackupsSistema"""
    class Meta:
        model = BackupsSistema
        fields = [
            'id', 'tipo_backup', 'estado', 'fecha_inicio', 'fecha_fin',
            'tamaño_mb', 'ubicacion_almacenamiento', 'duracion_minutos',
            'error_mensaje'
        ]
        read_only_fields = ['id', 'fecha_inicio']
