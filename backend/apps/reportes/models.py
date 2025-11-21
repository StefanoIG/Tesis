from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Reportes(models.Model):
    """
    Reportes generados por el sistema para análisis estratégico.
    """
    TIPOS_REPORTE = [
        ('TRAZABILIDAD', 'Trazabilidad de Lote'),
        ('PRODUCCION', 'Producción Total'),
        ('CALIDAD', 'Control de Calidad'),
        ('LOGISTICA', 'Logística y Transporte'),
        ('KPI', 'Indicadores Clave de Desempeño'),
        ('EXPORTACION', 'Exportaciones'),
        ('CUMPLIMIENTO', 'Cumplimiento Normativo'),
        ('EFICIENCIA', 'Eficiencia Operacional'),
        ('PERSONALIZADO', 'Personalizado'),
    ]

    FORMATOS_EXPORTACION = [
        ('PDF', 'PDF'),
        ('CSV', 'CSV'),
        ('EXCEL', 'Excel'),
        ('JSON', 'JSON'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    tipo_reporte = models.CharField(max_length=50, choices=TIPOS_REPORTE)
    
    # Usuario generador
    usuario_creador = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Filtros y parámetros
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    filtros_aplicados = models.JSONField(default=dict, blank=True)
    
    # Datos del reporte
    datos_reporte = models.JSONField(default=dict)
    
    # Archivo generado
    archivo_generado = models.FileField(upload_to='reportes/', null=True, blank=True)
    formato_exportacion = models.CharField(max_length=20, choices=FORMATOS_EXPORTACION, default='PDF')
    
    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reportes'
        verbose_name = _('Reporte')
        verbose_name_plural = _('Reportes')
        indexes = [
            models.Index(fields=['usuario_creador', 'creado_en']),
            models.Index(fields=['tipo_reporte']),
        ]

    def __str__(self):
        return self.nombre


class IndicesKPI(models.Model):
    """
    Indicadores clave de desempeño (KPI) calculados del sistema.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Indicadores de producción
    produccion_total_kg = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    numero_lotes_registrados = models.IntegerField(default=0)
    numero_productos_diferentes = models.IntegerField(default=0)
    
    # Indicadores de calidad
    porcentaje_aprobados = models.FloatField(default=0.0)
    porcentaje_rechazados = models.FloatField(default=0.0)
    porcentaje_condicionados = models.FloatField(default=0.0)
    
    # Indicadores logísticos
    entregas_a_tiempo = models.IntegerField(default=0)
    entregas_retrasadas = models.IntegerField(default=0)
    tiempo_promedio_transporte_horas = models.FloatField(default=0.0)
    
    # Indicadores de cumplimiento
    certificaciones_activas = models.IntegerField(default=0)
    porcentaje_cumplimiento_normativo = models.FloatField(default=0.0)
    incidencias_reportadas = models.IntegerField(default=0)
    
    # Período de los datos
    fecha_inicio_periodo = models.DateField()
    fecha_fin_periodo = models.DateField()
    
    # Auditoría
    calculado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'indices_kpi'
        verbose_name = _('Índice KPI')
        verbose_name_plural = _('Índices KPI')
        indexes = [
            models.Index(fields=['fecha_inicio_periodo', 'fecha_fin_periodo']),
        ]

    def __str__(self):
        return f"KPI {self.fecha_inicio_periodo} - {self.fecha_fin_periodo}"


class DashboardDatos(models.Model):
    """
    Datos precalculados para los dashboards del sistema.
    Mejora el rendimiento de visualización de datos.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # Tipos de datos
    tipo_dashboard = models.CharField(
        max_length=50,
        choices=[
            ('PRODUCTOR', 'Dashboard Productor'),
            ('GERENTE_OPERACIONES', 'Dashboard Gerente Operaciones'),
            ('GERENTE_CALIDAD', 'Dashboard Gerente Calidad'),
            ('ADMIN_SISTEMA', 'Dashboard Administrador'),
        ]
    )
    
    # Datos del dashboard
    datos = models.JSONField(default=dict)
    
    # Control
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dashboard_datos'
        verbose_name = _('Dashboard Datos')
        verbose_name_plural = _('Dashboards Datos')

    def __str__(self):
        return f"{self.tipo_dashboard} - {self.usuario}"
