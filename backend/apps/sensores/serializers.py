from rest_framework import serializers
from .models import (
    DispositivosSensores, LecturasSensores,
    ConfiguracionesAlertasSensor, RegistrosMantenimientoSensor
)


class DispositivosSensoresSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    finca_nombre = serializers.CharField(source='finca.nombre', read_only=True)
    ubicacion_nombre = serializers.CharField(source='ubicacion.nombre', read_only=True)
    ultima_lectura = serializers.SerializerMethodField()

    class Meta:
        model = DispositivosSensores
        fields = [
            'id', 'codigo_dispositivo', 'nombre', 'tipo_dispositivo',
            'empresa', 'empresa_nombre',
            'finca', 'finca_nombre',
            'ubicacion', 'ubicacion_nombre',
            'latitud', 'longitud', 'descripcion_ubicacion',
            'fabricante', 'modelo', 'numero_serie', 'firmware_version',
            'frecuencia_lectura_minutos', 'umbral_alerta_min', 'umbral_alerta_max',
            'estado', 'fecha_instalacion', 'fecha_ultimo_mantenimiento',
            'fecha_proximo_mantenimiento', 'ultima_lectura_fecha', 'ultima_lectura',
            'ip_address', 'mac_address',
            'configuracion_adicional', 'notas',
            'creado_en', 'actualizado_en'
        ]

    def get_ultima_lectura(self, obj):
        lectura = obj.lecturas.first()
        if lectura:
            return {
                'valor': float(lectura.valor),
                'unidad': lectura.unidad_medida,
                'fecha': lectura.fecha_lectura
            }
        return None


class LecturasSensoresSerializer(serializers.ModelSerializer):
    dispositivo_codigo = serializers.CharField(source='dispositivo.codigo_dispositivo', read_only=True)
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    registrado_por_nombre = serializers.CharField(source='registrado_por.nombre_completo', read_only=True)

    class Meta:
        model = LecturasSensores
        fields = [
            'id', 'dispositivo', 'dispositivo_codigo',
            'lote', 'lote_codigo',
            'transporte', 'ubicacion',
            'tipo_medicion', 'valor', 'unidad_medida',
            'fecha_lectura', 'fuente',
            'latitud', 'longitud',
            'registrado_por', 'registrado_por_nombre',
            'alerta_generada', 'fuera_de_rango',
            'datos_adicionales', 'observaciones',
            'creado_en'
        ]


class LecturaSensorCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear lecturas manuales."""
    
    class Meta:
        model = LecturasSensores
        fields = [
            'dispositivo', 'lote', 'transporte', 'ubicacion',
            'tipo_medicion', 'valor', 'unidad_medida',
            'fecha_lectura', 'latitud', 'longitud',
            'observaciones'
        ]

    def create(self, validated_data):
        validated_data['fuente'] = 'MANUAL'
        validated_data['registrado_por'] = self.context['request'].user
        return super().create(validated_data)


class ConfiguracionesAlertasSensorSerializer(serializers.ModelSerializer):
    dispositivo_codigo = serializers.CharField(source='dispositivo.codigo_dispositivo', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    usuarios_notificar_detalle = serializers.SerializerMethodField()

    class Meta:
        model = ConfiguracionesAlertasSensor
        fields = [
            'id', 'dispositivo', 'dispositivo_codigo',
            'empresa', 'empresa_nombre',
            'tipo_medicion', 'nombre', 'descripcion',
            'tipo_condicion', 'valor_referencia', 'valor_referencia_max',
            'nivel_alerta', 'mensaje_alerta', 'enviar_notificacion',
            'usuarios_notificar', 'usuarios_notificar_detalle',
            'es_activa',
            'creado_en', 'actualizado_en'
        ]

    def get_usuarios_notificar_detalle(self, obj):
        return [
            {
                'id': str(u.id),
                'email': u.email,
                'nombre': u.nombre_completo
            }
            for u in obj.usuarios_notificar.all()
        ]


class RegistrosMantenimientoSensorSerializer(serializers.ModelSerializer):
    dispositivo_codigo = serializers.CharField(source='dispositivo.codigo_dispositivo', read_only=True)
    registrado_por_nombre = serializers.CharField(source='registrado_por.nombre_completo', read_only=True)

    class Meta:
        model = RegistrosMantenimientoSensor
        fields = [
            'id', 'dispositivo', 'dispositivo_codigo',
            'tipo_mantenimiento', 'fecha_mantenimiento', 'descripcion',
            'tecnico_nombre', 'tecnico_empresa',
            'costo', 'resultado', 'repuestos_utilizados',
            'proximo_mantenimiento',
            'registrado_por', 'registrado_por_nombre',
            'creado_en', 'actualizado_en'
        ]
