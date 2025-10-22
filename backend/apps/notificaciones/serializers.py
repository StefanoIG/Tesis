from rest_framework import serializers
from apps.notificaciones.models import Notificaciones, PreferenciasNotificaciones, HistorialLecturaNotifc


class NotificacionesSerializer(serializers.ModelSerializer):
    """Serializer para Notificaciones"""
    class Meta:
        model = Notificaciones
        fields = [
            'id', 'usuario_destinatario', 'tipo_notificacion', 'titulo',
            'cuerpo', 'prioridad', 'alerta', 'evento_trazabilidad',
            'envio', 'lote', 'datos_adicionales', 'fue_leida',
            'fecha_lectura', 'fecha_expiracion', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


class NotificacionesNoLeidasSerializer(serializers.ModelSerializer):
    """Serializer simplificado para notificaciones no leídas (usado en polling)"""
    class Meta:
        model = Notificaciones
        fields = [
            'id', 'tipo_notificacion', 'titulo', 'cuerpo', 'prioridad',
            'datos_adicionales', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']


class PreferenciasNotificacionesSerializer(serializers.ModelSerializer):
    """Serializer para PreferenciasNotificaciones"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = PreferenciasNotificaciones
        fields = [
            'id', 'usuario', 'usuario_email', 'alertas_habilitadas',
            'eventos_trazabilidad_habilitados', 'estados_envios_habilitados',
            'calidad_habilitada', 'sincronizacion_habilitada', 'sistema_habilitada',
            'intervalo_polling_segundos', 'eliminar_notificaciones_leidas_dias',
            'silencioso_horario_inicio', 'silencioso_horario_fin', 'actualizado_en'
        ]
        read_only_fields = ['id', 'usuario', 'actualizado_en']


class HistorialLecturaNotificacionesSerializer(serializers.ModelSerializer):
    """Serializer para HistorialLecturaNotifc"""
    notificacion_titulo = serializers.CharField(source='notificacion.titulo', read_only=True)

    class Meta:
        model = HistorialLecturaNotifc
        fields = [
            'id', 'notificacion', 'notificacion_titulo', 'tipo_dispositivo',
            'codigo_dispositivo', 'timestamp_lectura', 'ip_dispositivo', 'user_agent'
        ]
        read_only_fields = ['id', 'timestamp_lectura']
