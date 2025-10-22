from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Documentos(models.Model):
    """
    Gestión de documentos y evidencias que acompañan la trazabilidad.
    """
    TIPOS_DOCUMENTO = [
        ('CERTIFICADO', 'Certificado'),
        ('RESULTADO_LABORATORIO', 'Resultado de Laboratorio'),
        ('FACTURA', 'Factura'),
        ('GUIA_TRANSPORTE', 'Guía de Transporte'),
        ('FOTO', 'Foto'),
        ('INFORME', 'Informe'),
        ('REPORTE_INSPECCION', 'Reporte de Inspección'),
        ('OTRO', 'Otro'),
    ]

    ESTADOS_DOCUMENTO = [
        ('PENDIENTE', 'Pendiente'),
        ('VALIDADO', 'Validado'),
        ('RECHAZADO', 'Rechazado'),
        ('ARCHIVADO', 'Archivado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Referencia a entidades
    lote = models.ForeignKey(
        'trazabilidad.Lotes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documentos'
    )
    evento_trazabilidad = models.ForeignKey(
        'trazabilidad.EventosTrazabilidad',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documentos'
    )
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Información del documento
    tipo_documento = models.CharField(max_length=50, choices=TIPOS_DOCUMENTO)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    
    # Archivo
    archivo = models.FileField(upload_to='documentos/', max_length=500)
    tipo_archivo = models.CharField(max_length=20)  # pdf, jpg, png, doc, etc
    tamaño_bytes = models.BigIntegerField(null=True, blank=True)
    
    # Validación
    estado = models.CharField(max_length=20, choices=ESTADOS_DOCUMENTO, default='PENDIENTE')
    es_autentico = models.BooleanField(default=False)
    hash_documento = models.CharField(max_length=256, null=True, blank=True, help_text="SHA-256 para verificación")
    
    # Información adicional
    fecha_documento = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    numero_referencia = models.CharField(max_length=100, blank=True, null=True)
    
    # Auditoría
    subido_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documentos_subidos'
    )
    validado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documentos_validados'
    )
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    comentarios_validacion = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'documentos'
        verbose_name = _('Documento')
        verbose_name_plural = _('Documentos')
        indexes = [
            models.Index(fields=['lote']),
            models.Index(fields=['evento_trazabilidad']),
            models.Index(fields=['tipo_documento']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return self.nombre


class FotosProductos(models.Model):
    """
    Registro específico para fotos de productos.
    Se usa para documentar el estado visual de los lotes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey('trazabilidad.Lotes', on_delete=models.CASCADE, related_name='fotos')
    
    # Foto
    imagen = models.ImageField(upload_to='fotos_productos/')
    
    # Metadata
    descripcion = models.TextField(blank=True, null=True)
    tipo_foto = models.CharField(
        max_length=50,
        choices=[
            ('INICIAL', 'Foto Inicial'),
            ('PROCESAMIENTO', 'Durante Procesamiento'),
            ('FINAL', 'Foto Final'),
            ('INSPECCION', 'Inspección'),
            ('TRANSPORTE', 'Transporte'),
        ]
    )
    
    # Ubicación
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    
    # Auditoría
    fotógrafo = models.ForeignKey('autenticacion.Usuarios', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_foto = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fotos_productos'
        verbose_name = _('Foto Producto')
        verbose_name_plural = _('Fotos Productos')

    def __str__(self):
        return f"{self.lote.codigo_lote} - {self.tipo_foto}"
