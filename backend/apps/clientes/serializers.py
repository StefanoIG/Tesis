from rest_framework import serializers
from .models import (
    Clientes, Ventas, DetallesVenta, Cotizaciones,
    HistorialInteraccionesCliente
)


class ClientesSerializer(serializers.ModelSerializer):
    total_ventas = serializers.SerializerMethodField()
    ultima_venta = serializers.SerializerMethodField()

    class Meta:
        model = Clientes
        fields = [
            'id', 'nombre_comercial', 'razon_social', 'tipo_cliente', 'categoria',
            'identificacion_fiscal', 'email', 'telefono', 'telefono_alternativo',
            'direccion', 'ciudad', 'provincia_estado', 'pais', 'codigo_postal',
            'limite_credito', 'dias_credito', 'descuento_porcentaje',
            'contacto_nombre', 'contacto_cargo', 'contacto_email', 'contacto_telefono',
            'certificaciones_requeridas', 'requisitos_especiales',
            'es_activo', 'fecha_primer_contacto', 'fecha_primera_venta',
            'total_ventas', 'ultima_venta',
            'notas', 'creado_en', 'actualizado_en'
        ]

    def get_total_ventas(self, obj):
        return obj.ventas.filter(estado__in=['CONFIRMADA', 'ENVIADA', 'ENTREGADA', 'FACTURADA']).count()

    def get_ultima_venta(self, obj):
        venta = obj.ventas.filter(estado__in=['CONFIRMADA', 'ENVIADA', 'ENTREGADA', 'FACTURADA']).first()
        return venta.fecha_venta if venta else None


class DetallesVentaSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    producto_nombre = serializers.CharField(source='lote.producto.nombre', read_only=True)

    class Meta:
        model = DetallesVenta
        fields = [
            'id', 'venta', 'lote', 'lote_codigo', 'producto_nombre',
            'cantidad', 'unidad_medida',
            'precio_unitario', 'descuento_porcentaje', 'descuento_monto',
            'subtotal', 'descripcion', 'notas',
            'creado_en'
        ]


class VentasSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre_comercial', read_only=True)
    vendedor_nombre = serializers.CharField(source='vendedor.nombre_completo', read_only=True)
    detalles = DetallesVentaSerializer(many=True, read_only=True)
    cantidad_items = serializers.SerializerMethodField()

    class Meta:
        model = Ventas
        fields = [
            'id', 'numero_venta', 'numero_factura',
            'cliente', 'cliente_nombre',
            'vendedor', 'vendedor_nombre',
            'fecha_venta', 'fecha_entrega_estimada', 'fecha_entrega_real',
            'estado', 'condicion_pago', 'incoterm',
            'subtotal', 'descuento', 'impuestos', 'total', 'moneda',
            'direccion_entrega', 'transporte_asignado',
            'observaciones', 'terminos_condiciones',
            'detalles', 'cantidad_items', 'metadata_adicional',
            'creado_en', 'actualizado_en'
        ]

    def get_cantidad_items(self, obj):
        return obj.detalles.count()


class VentaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear ventas con detalles."""
    
    detalles = DetallesVentaSerializer(many=True, required=False)

    class Meta:
        model = Ventas
        fields = [
            'numero_venta', 'cliente', 'vendedor',
            'fecha_venta', 'fecha_entrega_estimada',
            'estado', 'condicion_pago', 'incoterm',
            'subtotal', 'descuento', 'impuestos', 'total', 'moneda',
            'direccion_entrega', 'observaciones', 'terminos_condiciones',
            'detalles'
        ]

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        venta = Ventas.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetallesVenta.objects.create(venta=venta, **detalle_data)
        
        venta.calcular_total()
        venta.save()
        
        return venta


class CotizacionesSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre_comercial', read_only=True)
    vendedor_nombre = serializers.CharField(source='vendedor.nombre_completo', read_only=True)
    venta_generada_numero = serializers.CharField(source='venta_generada.numero_venta', read_only=True)
    dias_validez = serializers.SerializerMethodField()

    class Meta:
        model = Cotizaciones
        fields = [
            'id', 'numero_cotizacion',
            'cliente', 'cliente_nombre',
            'vendedor', 'vendedor_nombre',
            'fecha_cotizacion', 'fecha_validez', 'dias_validez',
            'estado', 'total', 'moneda',
            'condiciones_pago', 'tiempo_entrega_dias',
            'venta_generada', 'venta_generada_numero',
            'observaciones',
            'creado_en', 'actualizado_en'
        ]

    def get_dias_validez(self, obj):
        from django.utils import timezone
        if obj.fecha_validez:
            dias = (obj.fecha_validez - timezone.now().date()).days
            return dias
        return None


class HistorialInteraccionesClienteSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre_comercial', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)

    class Meta:
        model = HistorialInteraccionesCliente
        fields = [
            'id', 'cliente', 'cliente_nombre',
            'tipo_interaccion', 'fecha_interaccion',
            'asunto', 'descripcion',
            'usuario', 'usuario_nombre',
            'requiere_seguimiento', 'fecha_seguimiento',
            'seguimiento_completado', 'archivos_adjuntos',
            'creado_en'
        ]
