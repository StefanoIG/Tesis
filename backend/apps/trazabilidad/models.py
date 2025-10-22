from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


class Productos(models.Model):
    """
    Catálogo de productos que se pueden trazabilizar.
    Define los tipos de productos permitidos en el sistema.
    """
    TIPOS_PRODUCTO = [
        ('FRUTA', 'Fruta'),
        ('VERDURA', 'Verdura'),
        ('TUBÉRCULO', 'Tubérculo'),
        ('GRANO', 'Grano'),
        ('PROCESADO', 'Producto Procesado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    tipo_producto = models.CharField(max_length=50, choices=TIPOS_PRODUCTO)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=20, default='kg')  # kg, toneladas, cajas, etc.
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productos'
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')

    def __str__(self):
        return self.nombre


class Lotes(models.Model):
    """
    Registro de lotes de producción.
    Representa una unidad trazable de producto desde origen hasta destino final.
    """
    ESTADOS_LOTE = [
        ('PRODUCCION', 'En Producción'),
        ('ALMACENADO', 'Almacenado'),
        ('TRANSITO', 'En Tránsito'),
        ('PROCESAMIENTO', 'En Procesamiento'),
        ('CALIDAD_PENDIENTE', 'Calidad Pendiente'),
        ('CALIDAD_RECHAZADO', 'Calidad Rechazado'),
        ('EXPORTACION', 'Exportado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_lote = models.CharField(max_length=100, unique=True, db_index=True)
    producto = models.ForeignKey(Productos, on_delete=models.PROTECT, related_name='lotes')
    cantidad = models.DecimalField(max_digits=15, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    
    # Información de origen
    latitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    nombre_ubicacion_origen = models.CharField(max_length=255, blank=True, null=True)
    
    # Fechas
    fecha_produccion = models.DateTimeField()
    fecha_empaque = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    
    # Estado y control
    estado = models.CharField(max_length=30, choices=ESTADOS_LOTE, default='PRODUCCION')
    es_organico = models.BooleanField(default=False)
    
    # Información de calidad
    temperatura_almacenamiento = models.FloatField(null=True, blank=True, help_text="En grados Celsius")
    humedad_almacenamiento = models.FloatField(null=True, blank=True, help_text="En porcentaje")
    
    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    class Meta:
        db_table = 'lotes'
        verbose_name = _('Lote')
        verbose_name_plural = _('Lotes')
        indexes = [
            models.Index(fields=['codigo_lote']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_produccion']),
            models.Index(fields=['producto', 'estado']),
        ]

    def __str__(self):
        return f"{self.codigo_lote} - {self.producto.nombre}"

    def generar_qr(self):
        """Genera código QR para el lote"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"LOTE:{self.codigo_lote}:ID:{self.id}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        file_name = f"qr_{self.codigo_lote}.png"
        file_path = BytesIO()
        img.save(file_path, format='PNG')
        file_path.seek(0)
        self.qr_code.save(file_name, ContentFile(file_path.read()), save=False)


class TiposEventosTrazabilidad(models.Model):
    """
    Define los tipos de eventos que pueden registrarse en la trazabilidad.
    Ejemplos: cosecha, transporte, inspección, almacenamiento, etc.
    """
    CATEGORIAS_EVENTO = [
        ('PRODUCCION', 'Producción'),
        ('INSPECCION', 'Inspección'),
        ('PROCESAMIENTO', 'Procesamiento'),
        ('TRANSPORTE', 'Transporte'),
        ('ALMACENAMIENTO', 'Almacenamiento'),
        ('CALIDAD', 'Control de Calidad'),
        ('EXPORTACION', 'Exportación'),
        ('RECEPCION', 'Recepción'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS_EVENTO)
    descripcion = models.TextField(blank=True, null=True)
    requiere_documento = models.BooleanField(default=False)
    requiere_foto = models.BooleanField(default=False)
    requiere_gps = models.BooleanField(default=False)

    class Meta:
        db_table = 'tipos_eventos_trazabilidad'
        verbose_name = _('Tipo de Evento Trazabilidad')
        verbose_name_plural = _('Tipos de Eventos Trazabilidad')

    def __str__(self):
        return self.nombre


class EventosTrazabilidad(models.Model):
    """
    Registro de cada evento en el ciclo de vida del lote.
    Forma la cadena de custodia digital del producto.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey(Lotes, on_delete=models.CASCADE, related_name='eventos')
    tipo_evento = models.ForeignKey(TiposEventosTrazabilidad, on_delete=models.PROTECT)
    
    # Usuario responsable del evento
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Ubicación del evento
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    nombre_ubicacion = models.CharField(max_length=255, blank=True, null=True)
    
    # Detalles del evento
    descripcion = models.TextField()
    fecha_evento = models.DateTimeField()
    observaciones = models.TextField(blank=True, null=True)
    
    # Metadata técnica
    temperatura_registrada = models.FloatField(null=True, blank=True)
    humedad_registrada = models.FloatField(null=True, blank=True)
    
    # Auditoría
    timestamp_registro = models.DateTimeField(auto_now_add=True)
    es_sincronizado = models.BooleanField(default=False, help_text="Indica si viene del dispositivo móvil")

    class Meta:
        db_table = 'eventos_trazabilidad'
        verbose_name = _('Evento Trazabilidad')
        verbose_name_plural = _('Eventos Trazabilidad')
        indexes = [
            models.Index(fields=['lote', 'fecha_evento']),
            models.Index(fields=['tipo_evento', 'fecha_evento']),
            models.Index(fields=['timestamp_registro']),
        ]

    def __str__(self):
        return f"{self.lote.codigo_lote} - {self.tipo_evento.nombre} - {self.fecha_evento}"


class HistorialEstadosLote(models.Model):
    """
    Historial completo de cambios de estado de cada lote.
    Permite auditoría y trazabilidad de transiciones.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey(Lotes, on_delete=models.CASCADE, related_name='cambios_estado')
    estado_anterior = models.CharField(max_length=30)
    estado_nuevo = models.CharField(max_length=30)
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    motivo = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_estados_lote'
        verbose_name = _('Historial Estados Lote')
        verbose_name_plural = _('Historiales Estados Lote')
        indexes = [
            models.Index(fields=['lote', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.lote.codigo_lote}: {self.estado_anterior} -> {self.estado_nuevo}"
