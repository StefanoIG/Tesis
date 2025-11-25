from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Clientes(models.Model):
    """
    Registro de clientes (compradores) de productos agroindustriales.
    """
    TIPOS_CLIENTE = [
        ('DISTRIBUIDOR', 'Distribuidor'),
        ('EXPORTADOR', 'Exportador'),
        ('INDUSTRIA', 'Industria Procesadora'),
        ('RETAIL', 'Retail/Supermercado'),
        ('MAYORISTA', 'Mayorista'),
        ('MINORISTA', 'Minorista'),
        ('CONSUMIDOR_FINAL', 'Consumidor Final'),
        ('OTRO', 'Otro'),
    ]

    CATEGORIAS_CLIENTE = [
        ('A', 'Categoría A - Premium'),
        ('B', 'Categoría B - Regular'),
        ('C', 'Categoría C - Ocasional'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Información básica
    nombre_comercial = models.CharField(max_length=255)
    razon_social = models.CharField(max_length=255, blank=True, null=True)
    tipo_cliente = models.CharField(max_length=30, choices=TIPOS_CLIENTE)
    categoria = models.CharField(max_length=1, choices=CATEGORIAS_CLIENTE, default='B')
    
    # Identificación fiscal
    identificacion_fiscal = models.CharField(
        max_length=50,
        unique=True,
        help_text="RUC, RFC, Tax ID, etc."
    )
    
    # Contacto
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    telefono_alternativo = models.CharField(max_length=20, blank=True, null=True)
    
    # Ubicación
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    provincia_estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    
    # Información comercial
    limite_credito = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    dias_credito = models.IntegerField(
        default=0,
        help_text="Días de crédito otorgados"
    )
    descuento_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Descuento habitual en porcentaje"
    )
    
    # Persona de contacto
    contacto_nombre = models.CharField(max_length=100, blank=True, null=True)
    contacto_cargo = models.CharField(max_length=100, blank=True, null=True)
    contacto_email = models.EmailField(blank=True, null=True)
    contacto_telefono = models.CharField(max_length=20, blank=True, null=True)
    
    # Requisitos especiales
    certificaciones_requeridas = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de certificaciones que requiere"
    )
    requisitos_especiales = models.TextField(blank=True, null=True)
    
    # Estado
    es_activo = models.BooleanField(default=True)
    fecha_primer_contacto = models.DateField(null=True, blank=True)
    fecha_primera_venta = models.DateField(null=True, blank=True)
    
    # Observaciones
    notas = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clientes'
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')
        ordering = ['nombre_comercial']
        indexes = [
            models.Index(fields=['identificacion_fiscal']),
            models.Index(fields=['tipo_cliente', 'es_activo']),
            models.Index(fields=['pais', 'ciudad']),
        ]

    def __str__(self):
        return f"{self.nombre_comercial} ({self.tipo_cliente})"


class Ventas(models.Model):
    """
    Registro de ventas/órdenes de venta de lotes.
    """
    ESTADOS_VENTA = [
        ('COTIZACION', 'Cotización'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_PREPARACION', 'En Preparación'),
        ('ENVIADA', 'Enviada'),
        ('ENTREGADA', 'Entregada'),
        ('FACTURADA', 'Facturada'),
        ('CANCELADA', 'Cancelada'),
    ]

    CONDICIONES_PAGO = [
        ('CONTADO', 'Contado'),
        ('CREDITO_15', 'Crédito 15 días'),
        ('CREDITO_30', 'Crédito 30 días'),
        ('CREDITO_60', 'Crédito 60 días'),
        ('CREDITO_90', 'Crédito 90 días'),
        ('ANTICIPO_50', 'Anticipo 50%'),
        ('ANTICIPO_100', 'Anticipo 100%'),
    ]

    INCOTERMS = [
        ('EXW', 'EXW - Ex Works'),
        ('FCA', 'FCA - Free Carrier'),
        ('FOB', 'FOB - Free On Board'),
        ('CIF', 'CIF - Cost Insurance Freight'),
        ('DAP', 'DAP - Delivered at Place'),
        ('DDP', 'DDP - Delivered Duty Paid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Identificación
    numero_venta = models.CharField(max_length=50, unique=True, db_index=True)
    numero_factura = models.CharField(max_length=50, blank=True, null=True)
    
    # Relaciones
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.PROTECT,
        related_name='ventas'
    )
    vendedor = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas_realizadas'
    )
    
    # Fechas
    fecha_venta = models.DateField()
    fecha_entrega_estimada = models.DateField(null=True, blank=True)
    fecha_entrega_real = models.DateField(null=True, blank=True)
    
    # Estado y condiciones
    estado = models.CharField(max_length=20, choices=ESTADOS_VENTA, default='COTIZACION')
    condicion_pago = models.CharField(max_length=20, choices=CONDICIONES_PAGO, default='CONTADO')
    incoterm = models.CharField(max_length=10, choices=INCOTERMS, blank=True, null=True)
    
    # Valores
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=3, default='USD')
    
    # Logística
    direccion_entrega = models.TextField(blank=True, null=True)
    transporte_asignado = models.ForeignKey(
        'logistica.Transportes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas'
    )
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    terminos_condiciones = models.TextField(blank=True, null=True)
    
    # Metadata
    metadata_adicional = models.JSONField(default=dict, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ventas'
        verbose_name = _('Venta')
        verbose_name_plural = _('Ventas')
        ordering = ['-fecha_venta', '-numero_venta']
        indexes = [
            models.Index(fields=['numero_venta']),
            models.Index(fields=['cliente', 'estado']),
            models.Index(fields=['fecha_venta']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.numero_venta} - {self.cliente.nombre_comercial}"

    def calcular_total(self):
        """Calcula el total de la venta."""
        self.total = self.subtotal - self.descuento + self.impuestos
        return self.total


class DetallesVenta(models.Model):
    """
    Líneas de detalle de una venta (productos/lotes vendidos).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    venta = models.ForeignKey(
        Ventas,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    lote = models.ForeignKey(
        'trazabilidad.Lotes',
        on_delete=models.PROTECT,
        related_name='ventas'
    )
    
    # Cantidades
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    
    # Precios
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    descuento_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Información adicional
    descripcion = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'detalles_venta'
        verbose_name = _('Detalle de Venta')
        verbose_name_plural = _('Detalles de Venta')
        ordering = ['venta', 'creado_en']

    def __str__(self):
        return f"{self.venta.numero_venta} - {self.lote.codigo_lote}"

    def calcular_subtotal(self):
        """Calcula el subtotal de la línea."""
        subtotal_base = self.cantidad * self.precio_unitario
        self.subtotal = subtotal_base - self.descuento_monto
        return self.subtotal


class Cotizaciones(models.Model):
    """
    Cotizaciones previas a la venta.
    """
    ESTADOS_COTIZACION = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada al Cliente'),
        ('ACEPTADA', 'Aceptada'),
        ('RECHAZADA', 'Rechazada'),
        ('VENCIDA', 'Vencida'),
        ('CONVERTIDA', 'Convertida a Venta'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Identificación
    numero_cotizacion = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Relaciones
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.PROTECT,
        related_name='cotizaciones'
    )
    vendedor = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Fechas
    fecha_cotizacion = models.DateField()
    fecha_validez = models.DateField()
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADOS_COTIZACION, default='BORRADOR')
    
    # Valores
    total = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=3, default='USD')
    
    # Condiciones
    condiciones_pago = models.CharField(max_length=20, blank=True, null=True)
    tiempo_entrega_dias = models.IntegerField(null=True, blank=True)
    
    # Venta generada
    venta_generada = models.ForeignKey(
        Ventas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cotizacion_origen'
    )
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cotizaciones'
        verbose_name = _('Cotización')
        verbose_name_plural = _('Cotizaciones')
        ordering = ['-fecha_cotizacion']
        indexes = [
            models.Index(fields=['numero_cotizacion']),
            models.Index(fields=['cliente', 'estado']),
        ]

    def __str__(self):
        return f"{self.numero_cotizacion} - {self.cliente.nombre_comercial}"


class HistorialInteraccionesCliente(models.Model):
    """
    Registro de interacciones con clientes (CRM básico).
    """
    TIPOS_INTERACCION = [
        ('LLAMADA', 'Llamada Telefónica'),
        ('EMAIL', 'Correo Electrónico'),
        ('REUNION', 'Reunión'),
        ('VISITA', 'Visita a Cliente'),
        ('COTIZACION', 'Envío de Cotización'),
        ('RECLAMO', 'Reclamo'),
        ('SEGUIMIENTO', 'Seguimiento'),
        ('OTRO', 'Otro'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.CASCADE,
        related_name='interacciones'
    )
    
    # Información de la interacción
    tipo_interaccion = models.CharField(max_length=20, choices=TIPOS_INTERACCION)
    fecha_interaccion = models.DateTimeField()
    asunto = models.CharField(max_length=255)
    descripcion = models.TextField()
    
    # Usuario responsable
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Seguimiento
    requiere_seguimiento = models.BooleanField(default=False)
    fecha_seguimiento = models.DateField(null=True, blank=True)
    seguimiento_completado = models.BooleanField(default=False)
    
    # Archivos adjuntos
    archivos_adjuntos = models.JSONField(default=list, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_interacciones_cliente'
        verbose_name = _('Interacción con Cliente')
        verbose_name_plural = _('Interacciones con Clientes')
        ordering = ['-fecha_interaccion']
        indexes = [
            models.Index(fields=['cliente', 'fecha_interaccion']),
            models.Index(fields=['tipo_interaccion']),
            models.Index(fields=['requiere_seguimiento']),
        ]

    def __str__(self):
        return f"{self.cliente.nombre_comercial} - {self.tipo_interaccion} - {self.fecha_interaccion}"
