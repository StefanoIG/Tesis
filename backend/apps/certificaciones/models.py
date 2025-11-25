from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


class Certificaciones(models.Model):
    """
    Catálogo de tipos de certificaciones disponibles.
    Ejemplos: GlobalG.A.P., FSMA, BPA, Orgánico, Fair Trade, etc.
    """
    TIPOS_CERTIFICACION = [
        ('CALIDAD', 'Calidad'),
        ('ORGANICO', 'Orgánico'),
        ('AMBIENTAL', 'Ambiental'),
        ('SOCIAL', 'Social'),
        ('INOCUIDAD', 'Inocuidad Alimentaria'),
        ('BPA', 'Buenas Prácticas Agrícolas'),
        ('BPM', 'Buenas Prácticas de Manufactura'),
        ('COMERCIO_JUSTO', 'Comercio Justo'),
        ('OTRO', 'Otro'),
    ]

    ALCANCES = [
        ('INTERNACIONAL', 'Internacional'),
        ('NACIONAL', 'Nacional'),
        ('REGIONAL', 'Regional'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=30, unique=True, db_index=True)
    tipo_certificacion = models.CharField(max_length=30, choices=TIPOS_CERTIFICACION)
    entidad_emisora = models.CharField(max_length=100)
    alcance = models.CharField(max_length=20, choices=ALCANCES)
    
    # Información
    descripcion = models.TextField(blank=True, null=True)
    requisitos_generales = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Lista de requisitos generales para obtener la certificación"
    )
    url_informacion = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    
    # Vigencia
    vigencia_anios = models.IntegerField(
        default=1,
        help_text="Años de vigencia de la certificación"
    )
    
    # Control
    es_activa = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'certificaciones'
        verbose_name = _('Certificación')
        verbose_name_plural = _('Certificaciones')
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.entidad_emisora}"


class CertificacionesProductores(models.Model):
    """
    Certificaciones obtenidas por productores o asociaciones.
    """
    ESTADOS_CERTIFICACION = [
        ('VIGENTE', 'Vigente'),
        ('POR_RENOVAR', 'Por Renovar'),
        ('VENCIDA', 'Vencida'),
        ('SUSPENDIDA', 'Suspendida'),
        ('REVOCADA', 'Revocada'),
        ('EN_TRAMITE', 'En Trámite'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    certificacion = models.ForeignKey(
        Certificaciones,
        on_delete=models.PROTECT,
        related_name='productores_certificados'
    )
    
    # Puede ser asignada a un productor o a una asociación
    productor = models.ForeignKey(
        'usuarios.Empresas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='certificaciones_obtenidas',
        limit_choices_to={'tipo_empresa__in': ['PRODUCTOR', 'ASOCIACION']}
    )
    finca = models.ForeignKey(
        'usuarios.Fincas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='certificaciones',
        help_text="Certificación específica para una finca"
    )
    
    # Información del certificado
    numero_certificado = models.CharField(max_length=100, unique=True, db_index=True)
    fecha_emision = models.DateField()
    fecha_expiracion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CERTIFICACION, default='VIGENTE')
    
    # Documentos
    archivo_certificado = models.FileField(
        upload_to='certificaciones/',
        null=True,
        blank=True
    )
    
    # Alcance
    alcance_productos = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de productos cubiertos por esta certificación"
    )
    alcance_procesos = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de procesos cubiertos"
    )
    
    # Auditorías
    fecha_ultima_auditoria = models.DateField(null=True, blank=True)
    fecha_proxima_auditoria = models.DateField(null=True, blank=True)
    auditor_nombre = models.CharField(max_length=100, blank=True, null=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    condiciones_especiales = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'certificaciones_productores'
        verbose_name = _('Certificación de Productor')
        verbose_name_plural = _('Certificaciones de Productores')
        ordering = ['-fecha_emision']
        indexes = [
            models.Index(fields=['estado', 'fecha_expiracion']),
            models.Index(fields=['numero_certificado']),
            models.Index(fields=['productor', 'estado']),
        ]

    def __str__(self):
        entidad = self.productor.nombre if self.productor else "Sin productor"
        return f"{self.certificacion.nombre} - {entidad} - {self.numero_certificado}"

    def actualizar_estado(self):
        """Actualiza el estado basado en la fecha de expiración."""
        hoy = timezone.now().date()
        dias_para_expiracion = (self.fecha_expiracion - hoy).days
        
        if self.estado == 'VIGENTE':
            if dias_para_expiracion < 0:
                self.estado = 'VENCIDA'
            elif dias_para_expiracion <= 90:  # 3 meses
                self.estado = 'POR_RENOVAR'
        
        return self.estado


class CertificacionesLotes(models.Model):
    """
    Vincula lotes específicos con certificaciones del productor.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey(
        'trazabilidad.Lotes',
        on_delete=models.CASCADE,
        related_name='certificaciones_aplicadas'
    )
    certificacion_productor = models.ForeignKey(
        CertificacionesProductores,
        on_delete=models.PROTECT,
        related_name='lotes_certificados'
    )
    
    # Verificación
    verificado = models.BooleanField(default=False)
    verificado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    
    # Evidencia
    archivo_evidencia = models.FileField(
        upload_to='certificaciones/evidencias/',
        null=True,
        blank=True
    )
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificaciones_lotes'
        verbose_name = _('Certificación de Lote')
        verbose_name_plural = _('Certificaciones de Lotes')
        unique_together = ('lote', 'certificacion_productor')
        indexes = [
            models.Index(fields=['lote']),
            models.Index(fields=['verificado']),
        ]

    def __str__(self):
        return f"Lote {self.lote.codigo_lote} - {self.certificacion_productor.certificacion.nombre}"


class RequisitosCumplimiento(models.Model):
    """
    Requisitos normativos según certificación, normativa o país destino.
    """
    TIPOS_REQUISITO = [
        ('DOCUMENTACION', 'Documentación'),
        ('ANALISIS', 'Análisis de Laboratorio'),
        ('INSPECCION', 'Inspección'),
        ('REGISTRO', 'Registro'),
        ('PROCESO', 'Proceso Específico'),
        ('TRAZABILIDAD', 'Trazabilidad'),
        ('OTRO', 'Otro'),
    ]

    FRECUENCIAS = [
        ('UNICA_VEZ', 'Única Vez'),
        ('POR_LOTE', 'Por Lote'),
        ('MENSUAL', 'Mensual'),
        ('TRIMESTRAL', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relaciones
    certificacion = models.ForeignKey(
        Certificaciones,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='requisitos'
    )
    
    # Identificación del requisito
    codigo_requisito = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=200)
    normativa = models.CharField(max_length=100, blank=True, null=True)
    pais_destino = models.CharField(max_length=50, blank=True, null=True)
    
    # Detalle
    descripcion = models.TextField()
    tipo_requisito = models.CharField(max_length=30, choices=TIPOS_REQUISITO)
    es_obligatorio = models.BooleanField(default=True)
    frecuencia_verificacion = models.CharField(max_length=20, choices=FRECUENCIAS)
    
    # Documentación
    documentacion_requerida = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de documentos requeridos"
    )
    parametros_analisis = models.JSONField(
        default=dict,
        blank=True,
        help_text="Parámetros específicos si es un análisis"
    )
    
    # Control
    es_activo = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'requisitos_cumplimiento'
        verbose_name = _('Requisito de Cumplimiento')
        verbose_name_plural = _('Requisitos de Cumplimiento')
        ordering = ['normativa', 'nombre']
        indexes = [
            models.Index(fields=['normativa']),
            models.Index(fields=['pais_destino']),
            models.Index(fields=['codigo_requisito']),
        ]

    def __str__(self):
        return f"{self.codigo_requisito} - {self.nombre}"


class CumplimientoNormativo(models.Model):
    """
    Registro de cumplimiento de requisitos específicos por lote.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey(
        'trazabilidad.Lotes',
        on_delete=models.CASCADE,
        related_name='cumplimientos'
    )
    requisito = models.ForeignKey(
        RequisitosCumplimiento,
        on_delete=models.PROTECT,
        related_name='cumplimientos'
    )
    
    # Verificación
    cumplido = models.BooleanField()
    fecha_verificacion = models.DateTimeField()
    verificado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Evidencia
    evidencia_url = models.URLField(blank=True, null=True)
    archivo_evidencia = models.FileField(
        upload_to='cumplimiento/',
        null=True,
        blank=True
    )
    numero_referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Número de certificado, análisis, etc."
    )
    
    # Detalles
    observaciones = models.TextField(blank=True, null=True)
    datos_verificacion = models.JSONField(
        default=dict,
        blank=True,
        help_text="Datos específicos de la verificación"
    )
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cumplimiento_normativo'
        verbose_name = _('Cumplimiento Normativo')
        verbose_name_plural = _('Cumplimientos Normativos')
        unique_together = ('lote', 'requisito')
        ordering = ['-fecha_verificacion']
        indexes = [
            models.Index(fields=['lote', 'cumplido']),
            models.Index(fields=['requisito']),
        ]

    def __str__(self):
        return f"Lote {self.lote.codigo_lote} - {self.requisito.nombre} - {'✓' if self.cumplido else '✗'}"
