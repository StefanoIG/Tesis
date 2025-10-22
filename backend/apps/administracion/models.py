from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class ConfiguracionSistema(models.Model):
    """
    Parámetros de configuración global del sistema.
    """
    id = models.AutoField(primary_key=True)
    
    # Productos permitidos
    productos_permitidos = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de IDs de productos permitidos"
    )
    
    # Tipos de eventos
    tipos_eventos_permitidos = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de IDs de tipos de eventos permitidos"
    )
    
    # Unidades de medida
    unidades_medida = models.JSONField(
        default=dict,
        blank=True,
        help_text="Mapeo de unidades de medida"
    )
    
    # Configuración de notificaciones
    intervalo_sincronizacion_minutos = models.IntegerField(default=30)
    intervalo_notificaciones_minutos = models.IntegerField(default=5)
    
    # Configuración de almacenamiento
    tamaño_maximo_documento_mb = models.IntegerField(default=50)
    dias_retencion_documentos = models.IntegerField(default=2555, help_text="7 años por defecto")
    
    # Configuración de seguridad
    intentos_fallidos_max = models.IntegerField(default=5)
    bloqueo_minutos = models.IntegerField(default=15)
    sesion_duracion_horas = models.IntegerField(default=8)
    
    # Auditoría
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'configuracion_sistema'
        verbose_name = _('Configuración Sistema')
        verbose_name_plural = _('Configuración Sistema')

    def __str__(self):
        return "Configuración Global del Sistema"


class LogsAcceso(models.Model):
    """
    Registro de todos los accesos al sistema.
    """
    TIPOS_ACCESO = [
        ('EXITOSO', 'Exitoso'),
        ('FALLIDO', 'Fallido'),
        ('BLOQUEADO', 'Bloqueado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Información del acceso
    tipo_acceso = models.CharField(max_length=20, choices=TIPOS_ACCESO)
    ip_origen = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    
    # Motivo si es fallido
    motivo_fallo = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs_acceso'
        verbose_name = _('Log Acceso')
        verbose_name_plural = _('Logs Acceso')
        indexes = [
            models.Index(fields=['usuario', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.tipo_acceso} - {self.timestamp}"


class LogsActividad(models.Model):
    """
    Registro detallado de actividades de usuario en el sistema.
    """
    TIPOS_ACTIVIDAD = [
        ('CREATE', 'Crear'),
        ('UPDATE', 'Actualizar'),
        ('DELETE', 'Eliminar'),
        ('VIEW', 'Visualizar'),
        ('EXPORT', 'Exportar'),
        ('IMPORT', 'Importar'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey('autenticacion.Usuarios', on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo_actividad = models.CharField(max_length=20, choices=TIPOS_ACTIVIDAD)
    modulo = models.CharField(max_length=100)
    entidad = models.CharField(max_length=100)
    registro_id = models.CharField(max_length=100, null=True, blank=True)
    
    descripcion = models.TextField(blank=True, null=True)
    datos_antes = models.JSONField(null=True, blank=True)
    datos_despues = models.JSONField(null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs_actividad'
        verbose_name = _('Log Actividad')
        verbose_name_plural = _('Logs Actividad')
        indexes = [
            models.Index(fields=['usuario', 'timestamp']),
            models.Index(fields=['modulo']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.tipo_actividad} - {self.entidad}"


class BackupsSistema(models.Model):
    """
    Control de backups del sistema.
    """
    TIPOS_BACKUP = [
        ('COMPLETO', 'Backup Completo'),
        ('INCREMENTAL', 'Backup Incremental'),
        ('DIFERENCIAL', 'Backup Diferencial'),
    ]

    ESTADOS_BACKUP = [
        ('EXITOSO', 'Exitoso'),
        ('EN_PROGRESO', 'En Progreso'),
        ('FALLIDO', 'Fallido'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    tipo_backup = models.CharField(max_length=20, choices=TIPOS_BACKUP)
    estado = models.CharField(max_length=20, choices=ESTADOS_BACKUP)
    
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    tamaño_mb = models.FloatField(null=True, blank=True)
    ubicacion_almacenamiento = models.CharField(max_length=500, help_text="S3, Google Cloud, etc")
    
    duracion_minutos = models.FloatField(null=True, blank=True)
    error_mensaje = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'backups_sistema'
        verbose_name = _('Backup Sistema')
        verbose_name_plural = _('Backups Sistema')
        indexes = [
            models.Index(fields=['fecha_inicio']),
        ]

    def __str__(self):
        return f"{self.tipo_backup} - {self.estado} - {self.fecha_inicio}"
