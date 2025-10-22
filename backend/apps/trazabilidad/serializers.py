from rest_framework import serializers
from apps.trazabilidad.models import (
    Productos, Lotes, TiposEventosTrazabilidad,
    EventosTrazabilidad, HistorialEstadosLote
)


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Productos"""
    class Meta:
        model = Productos
        fields = ['id', 'nombre', 'tipo_producto', 'descripcion', 'unidad_medida', 'creado_en']
        read_only_fields = ['id', 'creado_en']


class TiposEventosTrazabilidadSerializer(serializers.ModelSerializer):
    """Serializer para TiposEventosTrazabilidad"""
    class Meta:
        model = TiposEventosTrazabilidad
        fields = [
            'id', 'nombre', 'categoria', 'descripcion',
            'requiere_documento', 'requiere_foto', 'requiere_gps'
        ]
        read_only_fields = ['id']


class HistorialEstadosLoteSerializer(serializers.ModelSerializer):
    """Serializer para el historial de cambios de estado"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = HistorialEstadosLote
        fields = [
            'id', 'lote', 'estado_anterior', 'estado_nuevo',
            'usuario', 'usuario_email', 'motivo', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class EventosTrazabilidadSerializer(serializers.ModelSerializer):
    """Serializer para EventosTrazabilidad"""
    tipo_evento_detalle = TiposEventosTrazabilidadSerializer(source='tipo_evento', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    ubicacion_coords = serializers.SerializerMethodField()

    class Meta:
        model = EventosTrazabilidad
        fields = [
            'id', 'lote', 'tipo_evento', 'tipo_evento_detalle',
            'usuario', 'usuario_email', 'latitud', 'longitud', 'ubicacion_coords',
            'nombre_ubicacion', 'descripcion', 'fecha_evento',
            'observaciones', 'temperatura_registrada', 'humedad_registrada',
            'timestamp_registro', 'es_sincronizado'
        ]
        read_only_fields = ['id', 'timestamp_registro']

    def get_ubicacion_coords(self, obj):
        if obj.latitud and obj.longitud:
            return {
                'latitude': float(obj.latitud),
                'longitude': float(obj.longitud),
            }
        return None


class LotesSerializer(serializers.ModelSerializer):
    """Serializer completo para Lotes"""
    producto_detalle = ProductoSerializer(source='producto', read_only=True)
    ubicacion_coords = serializers.SerializerMethodField()

    class Meta:
        model = Lotes
        fields = [
            'id', 'codigo_lote', 'producto', 'producto_detalle',
            'cantidad', 'unidad_medida', 'latitud_origen', 'longitud_origen', 'ubicacion_coords',
            'nombre_ubicacion_origen', 'fecha_produccion', 'fecha_empaque',
            'fecha_vencimiento', 'estado', 'es_organico',
            'temperatura_almacenamiento', 'humedad_almacenamiento',
            'creado_en', 'actualizado_en', 'qr_code'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en', 'qr_code']

    def get_ubicacion_coords(self, obj):
        if obj.latitud_origen and obj.longitud_origen:
            return {
                'latitude': float(obj.latitud_origen),
                'longitude': float(obj.longitud_origen),
            }
        return None


class LotesListaSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados de lotes"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = Lotes
        fields = [
            'id', 'codigo_lote', 'producto_nombre', 'cantidad',
            'unidad_medida', 'estado', 'fecha_produccion', 'actualizado_en'
        ]


class LotesConEventosSerializer(serializers.ModelSerializer):
    """Serializer para Lotes con historial de eventos"""
    producto_detalle = ProductoSerializer(source='producto', read_only=True)
    eventos = EventosTrazabilidadSerializer(many=True, read_only=True)
    cambios_estado = HistorialEstadosLoteSerializer(many=True, read_only=True)
    ubicacion_coords = serializers.SerializerMethodField()

    class Meta:
        model = Lotes
        fields = [
            'id', 'codigo_lote', 'producto', 'producto_detalle',
            'cantidad', 'unidad_medida', 'latitud_origen', 'longitud_origen', 'ubicacion_coords',
            'nombre_ubicacion_origen', 'fecha_produccion', 'fecha_empaque',
            'fecha_vencimiento', 'estado', 'es_organico',
            'temperatura_almacenamiento', 'humedad_almacenamiento',
            'eventos', 'cambios_estado', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = [
            'id', 'creado_en', 'actualizado_en', 'eventos', 'cambios_estado'
        ]

    def get_ubicacion_coords(self, obj):
        if obj.latitud_origen and obj.longitud_origen:
            return {
                'latitude': float(obj.latitud_origen),
                'longitude': float(obj.longitud_origen),
            }
        return None
