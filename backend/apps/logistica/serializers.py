from rest_framework import serializers
from apps.logistica.models import (
    Vehiculos, Conductores, Envios, RuteTrackingActual, AlertasLogistica
)


class VehiculosSerializer(serializers.ModelSerializer):
    """Serializer para Vehículos"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

    class Meta:
        model = Vehiculos
        fields = [
            'id', 'empresa', 'empresa_nombre', 'placa', 'tipo_vehiculo',
            'marca', 'modelo', 'año_fabricacion', 'capacidad_kg',
            'capacidad_volumen_m3', 'es_refrigerado', 'temperatura_min',
            'temperatura_max', 'estado', 'numero_seguro',
            'fecha_vencimiento_seguro', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


class ConductoresSerializer(serializers.ModelSerializer):
    """Serializer para Conductores"""
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

    class Meta:
        model = Conductores
        fields = [
            'id', 'usuario', 'usuario_nombre', 'usuario_email',
            'numero_licencia', 'categoria_licencia', 'fecha_vencimiento_licencia',
            'empresa', 'empresa_nombre', 'es_activo', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']


class RuteTrackingActualSerializer(serializers.ModelSerializer):
    """Serializer para RuteTrackingActual"""
    class Meta:
        model = RuteTrackingActual
        fields = [
            'id', 'envio', 'latitud', 'longitud',
            'temperatura', 'humedad', 'velocidad_kmh', 'timestamp', 'observaciones'
        ]
        read_only_fields = ['id', 'timestamp']


class AlertasLogisticaSerializer(serializers.ModelSerializer):
    """Serializer para AlertasLogistica"""
    class Meta:
        model = AlertasLogistica
        fields = [
            'id', 'envio', 'tipo_alerta', 'estado_alerta', 'descripcion',
            'fecha_alerta', 'fecha_resolucion', 'accion_tomada'
        ]
        read_only_fields = ['id', 'fecha_alerta']


class EnviosSerializer(serializers.ModelSerializer):
    """Serializer para Envíos"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    vehiculo_placa = serializers.CharField(source='vehiculo.placa', read_only=True, allow_null=True)
    conductor_nombre = serializers.CharField(source='conductor.usuario.nombre_completo', read_only=True, allow_null=True)
    tracking_actual = serializers.SerializerMethodField()

    class Meta:
        model = Envios
        fields = [
            'id', 'lote', 'lote_codigo', 'latitud_origen', 'longitud_origen', 'nombre_origen',
            'latitud_destino', 'longitud_destino', 'nombre_destino', 'vehiculo', 'vehiculo_placa',
            'conductor', 'conductor_nombre', 'fecha_salida', 'fecha_llegada_estimada',
            'fecha_llegada_real', 'temperatura_registrada', 'humedad_registrada',
            'distancia_km', 'estado', 'observaciones', 'incidencias',
            'tracking_actual', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']
        extra_kwargs = {
            'vehiculo': {'required': False, 'allow_null': True},
            'conductor': {'required': False, 'allow_null': True},
            'fecha_salida': {'required': False, 'allow_null': True},
        }

    def get_tracking_actual(self, obj):
        tracking = obj.tracking.latest('timestamp') if obj.tracking.exists() else None
        if tracking:
            return RuteTrackingActualSerializer(tracking).data
        return None


class EnviosConDetallesSerializer(serializers.ModelSerializer):
    """Serializer para Envíos con detalles completos"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    vehiculo_detalle = VehiculosSerializer(source='vehiculo', read_only=True)
    conductor_detalle = ConductoresSerializer(source='conductor', read_only=True)
    tracking = RuteTrackingActualSerializer(many=True, read_only=True)
    alertas = AlertasLogisticaSerializer(many=True, read_only=True)

    class Meta:
        model = Envios
        fields = [
            'id', 'lote', 'lote_codigo', 'latitud_origen', 'longitud_origen', 'nombre_origen',
            'latitud_destino', 'longitud_destino', 'nombre_destino', 'vehiculo', 'vehiculo_detalle',
            'conductor', 'conductor_detalle', 'fecha_salida', 'fecha_llegada_estimada',
            'fecha_llegada_real', 'temperatura_registrada', 'humedad_registrada',
            'distancia_km', 'estado', 'observaciones', 'incidencias',
            'tracking', 'alertas', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = [
            'id', 'creado_en', 'actualizado_en', 'tracking', 'alertas'
        ]
