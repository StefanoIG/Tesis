from rest_framework import serializers
from apps.sincronizacion.models import (
    EstadosSincronizacion, ConflictosSincronizacion,
    RegistrosSincronizacion, ControlVersionesDB
)


class EstadosSincronizacionSerializer(serializers.ModelSerializer):
    """Serializer para EstadosSincronizacion"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = EstadosSincronizacion
        fields = [
            'id', 'usuario', 'usuario_email', 'codigo_dispositivo', 'plataforma',
            'version_app', 'version_db_local', 'numero_registros_locales',
            'tamaño_db_local_mb', 'estado', 'ultimo_sync_exitoso',
            'ultimo_sync_intento', 'mensaje_error', 'reintentos',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


class ConflictosSincronizacionSerializer(serializers.ModelSerializer):
    """Serializer para ConflictosSincronizacion"""
    class Meta:
        model = ConflictosSincronizacion
        fields = [
            'id', 'sincronizacion', 'tabla_afectada', 'registro_id',
            'dato_cliente', 'dato_servidor', 'estrategia_resolucion',
            'estado_conflicto', 'dato_final', 'detectado_en', 'resuelto_en'
        ]
        read_only_fields = ['id', 'detectado_en']


class RegistrosSincronizacionSerializer(serializers.ModelSerializer):
    """Serializer para RegistrosSincronizacion"""
    class Meta:
        model = RegistrosSincronizacion
        fields = [
            'id', 'sincronizacion', 'tipo_sincronizacion',
            'registros_procesados', 'registros_exitosos', 'registros_fallidos',
            'registros_ignorados', 'datos_transferidos_mb', 'duracion_segundos',
            'fue_exitosa', 'mensaje', 'timestamp_inicio', 'timestamp_fin'
        ]
        read_only_fields = ['id', 'timestamp_inicio', 'timestamp_fin']


class ControlVersionesDBSerializer(serializers.ModelSerializer):
    """Serializer para ControlVersionesDB"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = ControlVersionesDB
        fields = [
            'id', 'usuario', 'usuario_email', 'numero_version',
            'descripcion_cambios', 'hash_schema', 'fecha_liberacion',
            'es_obligatoria', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']
