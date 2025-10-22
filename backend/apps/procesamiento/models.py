from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class ProcesosProcesamiento(models.Model):
    """
    Registro de procesos industriales realizados sobre lotes.
    """
    TIPOS_PROCESO = [
        ('LAVADO', 'Lavado'),
        ('CLASIFICACION', 'Clasificación'),
        ('EMPAQUETADO', 'Empaquetado'),
        ('TRANSFORMACION', 'Transformación'),
        ('CONGELACION', 'Congelación'),
        ('DESHIDRATACION', 'Deshidratación'),
        ('OTRO', 'Otro'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey('trazabilidad.Lotes', on_delete=models.CASCADE, related_name='procesos')
    empresa = models.ForeignKey('usuarios.Empresas', on_delete=models.PROTECT)
    
    tipo_proceso = models.CharField(max_length=50, choices=TIPOS_PROCESO)
    descripcion = models.TextField()
    
    # Fechas
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    # Responsable
    usuario_responsable = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Parámetros del proceso
    temperatura_promedio = models.FloatField(null=True, blank=True)
    humedad_promedio = models.FloatField(null=True, blank=True)
    tiempo_duracion_minutos = models.IntegerField(null=True, blank=True)
    
    # Control de calidad
    resultado_proceso = models.JSONField(default=dict, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'procesos_procesamiento'
        verbose_name = _('Proceso Procesamiento')
        verbose_name_plural = _('Procesos Procesamiento')
        indexes = [
            models.Index(fields=['lote', 'fecha_inicio']),
            models.Index(fields=['empresa', 'fecha_inicio']),
        ]

    def __str__(self):
        return f"{self.lote.codigo_lote} - {self.tipo_proceso}"


class InspeccionesCalidad(models.Model):
    """
    Inspecciones de control de calidad a lotes.
    """
    RESULTADOS_INSPECCION = [
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('CONDICIONADO', 'Condicionado'),
        ('PENDIENTE', 'Pendiente'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey('trazabilidad.Lotes', on_delete=models.CASCADE, related_name='inspecciones')
    empresa = models.ForeignKey('usuarios.Empresas', on_delete=models.PROTECT)
    
    inspector = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Tipo de inspección
    tipo_inspeccion = models.CharField(max_length=100, help_text="Ej: Inspección Sensorial, Análisis Físico")
    fecha_inspeccion = models.DateTimeField()
    
    # Resultado
    resultado = models.CharField(max_length=20, choices=RESULTADOS_INSPECCION, default='PENDIENTE')
    porcentaje_rechazo = models.FloatField(default=0.0, help_text="Porcentaje de producto rechazado")
    
    # Criterios evaluados
    criterios_evaluados = models.JSONField(
        default=dict,
        blank=True,
        help_text="Ej: {color: 'cumple', textura: 'cumple', olor: 'no_cumple'}"
    )
    
    observaciones = models.TextField(blank=True, null=True)
    recomendaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inspecciones_calidad'
        verbose_name = _('Inspección Calidad')
        verbose_name_plural = _('Inspecciones Calidad')
        indexes = [
            models.Index(fields=['lote', 'fecha_inspeccion']),
            models.Index(fields=['resultado']),
        ]

    def __str__(self):
        return f"{self.lote.codigo_lote} - {self.tipo_inspeccion} - {self.resultado}"


class CertificacionesEstandares(models.Model):
    """
    Certificaciones de cumplimiento normativo para lotes.
    """
    TIPOS_CERTIFICACION = [
        ('GLOBALG_A_P', 'GlobalG.A.P'),
        ('AGROCALIDAD', 'AGROCALIDAD'),
        ('ORGANICO', 'Orgánico'),
        ('BPA', 'Buenas Prácticas Agrícolas'),
        ('FSSC22000', 'FSSC 22000'),
        ('OTRA', 'Otra'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey('trazabilidad.Lotes', on_delete=models.CASCADE, related_name='certificaciones')
    empresa = models.ForeignKey('usuarios.Empresas', on_delete=models.PROTECT)
    
    tipo_certificacion = models.CharField(max_length=50, choices=TIPOS_CERTIFICACION)
    numero_certificado = models.CharField(max_length=100, unique=True)
    
    # Fechas de validez
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    
    # Información del certificador
    organismo_certificador = models.CharField(max_length=255)
    auditor = models.CharField(max_length=255, blank=True)
    
    # Archivos
    documento_certificado = models.FileField(upload_to='certificaciones/')
    
    # Estado
    es_valida = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificaciones_estandares'
        verbose_name = _('Certificación Estándar')
        verbose_name_plural = _('Certificaciones Estándares')

    def __str__(self):
        return f"{self.numero_certificado} - {self.tipo_certificacion}"


class ResultadosAnalisisLaboratorio(models.Model):
    """
    Resultados de análisis de laboratorio para control de calidad.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey('trazabilidad.Lotes', on_delete=models.CASCADE, related_name='analisis_laboratorio')
    empresa = models.ForeignKey('usuarios.Empresas', on_delete=models.PROTECT)
    
    # Información del análisis
    tipo_analisis = models.CharField(max_length=100, help_text="Ej: Análisis Microbiológico, Residuos de Pesticidas")
    laboratorio = models.CharField(max_length=255)
    fecha_muestreo = models.DateTimeField()
    fecha_resultado = models.DateTimeField()
    
    # Resultados
    parametros_medidos = models.JSONField(
        default=dict,
        blank=True,
        help_text="Ej: {E_coli: '< 10 UFC/g', Listeria: 'Ausente'}"
    )
    resultado_general = models.CharField(
        max_length=50,
        choices=[('CUMPLE', 'Cumple'), ('NO_CUMPLE', 'No Cumple')],
        default='PENDIENTE'
    )
    
    # Documentación
    numero_informe = models.CharField(max_length=100, unique=True)
    documento_informe = models.FileField(upload_to='analisis_laboratorio/')
    
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resultados_analisis_laboratorio'
        verbose_name = _('Resultado Análisis Laboratorio')
        verbose_name_plural = _('Resultados Análisis Laboratorio')

    def __str__(self):
        return f"{self.numero_informe} - {self.tipo_analisis}"
