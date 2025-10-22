from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class EstadosSincronizacion(models.Model):
    """
    Control del estado de sincronización por dispositivo/usuario.
    """
    ESTADOS_SINCRONIZACION = [
        ('SINCRONIZADO', 'Sincronizado'),
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('CONFLICTO', 'Conflicto'),
        ('ERROR', 'Error'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey('autenticacion.Usuarios', on_delete=models.CASCADE, related_name='sincronizaciones')
    
    # Identificación del dispositivo
    codigo_dispositivo = models.CharField(max_length=100, help_text="Identificador único del dispositivo móvil")
    plataforma = models.CharField(
        max_length=20,
        choices=[('ANDROID', 'Android'), ('IOS', 'iOS'), ('WEB', 'Web')]
    )
    version_app = models.CharField(max_length=20, blank=True, null=True)
    
    # Estado de la BD local
    version_db_local = models.CharField(max_length=20, blank=True, null=True)
    numero_registros_locales = models.IntegerField(default=0)
    tamaño_db_local_mb = models.FloatField(default=0.0)
    
    # Estado de sincronización
    estado = models.CharField(max_length=20, choices=ESTADOS_SINCRONIZACION, default='SINCRONIZADO')
    ultimo_sync_exitoso = models.DateTimeField(null=True, blank=True)
    ultimo_sync_intento = models.DateTimeField(null=True, blank=True)
    
    # Detalles de errores
    mensaje_error = models.TextField(blank=True, null=True)
    reintentos = models.IntegerField(default=0)
    
    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estados_sincronizacion'
        verbose_name = _('Estado Sincronización')
        verbose_name_plural = _('Estados Sincronización')
        unique_together = ('usuario', 'codigo_dispositivo')

    def __str__(self):
        return f"{self.usuario.email} - {self.codigo_dispositivo}"


class ConflictosSincronizacion(models.Model):
    """
    Registro de conflictos detectados durante sincronización.
    """
    ESTRATEGIAS_RESOLUCION = [
        ('ULTIMA_ESCRITURA', 'Última Escritura Gana'),
        ('CLIENTE', 'Versión Cliente'),
        ('SERVIDOR', 'Versión Servidor'),
        ('MANUAL', 'Resolución Manual'),
    ]

    ESTADOS_CONFLICTO = [
        ('ABIERTO', 'Abierto'),
        ('RESUELTO', 'Resuelto'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sincronizacion = models.ForeignKey(
        EstadosSincronizacion,
        on_delete=models.CASCADE,
        related_name='conflictos'
    )
    
    # Información del conflicto
    tabla_afectada = models.CharField(max_length=100)
    registro_id = models.CharField(max_length=100)
    
    # Datos en conflicto
    dato_cliente = models.JSONField()
    dato_servidor = models.JSONField()
    
    # Resolución
    estrategia_resolucion = models.CharField(
        max_length=20,
        choices=ESTRATEGIAS_RESOLUCION,
        default='ULTIMA_ESCRITURA'
    )
    estado_conflicto = models.CharField(
        max_length=20,
        choices=ESTADOS_CONFLICTO,
        default='ABIERTO'
    )
    dato_final = models.JSONField(null=True, blank=True)
    
    # Auditoría
    detectado_en = models.DateTimeField(auto_now_add=True)
    resuelto_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'conflictos_sincronizacion'
        verbose_name = _('Conflicto Sincronización')
        verbose_name_plural = _('Conflictos Sincronización')

    def __str__(self):
        return f"Conflicto - {self.tabla_afectada} - {self.registro_id}"


class RegistrosSincronizacion(models.Model):
    """
    Log detallado de cada evento de sincronización.
    """
    TIPOS_SINCRONIZACION = [
        ('UPLOAD', 'Carga a Servidor'),
        ('DOWNLOAD', 'Descarga del Servidor'),
        ('BIDIRECIONAL', 'Bidireccional'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sincronizacion = models.ForeignKey(
        EstadosSincronizacion,
        on_delete=models.CASCADE,
        related_name='registros'
    )
    
    # Tipo de sincronización
    tipo_sincronizacion = models.CharField(max_length=20, choices=TIPOS_SINCRONIZACION)
    
    # Estadísticas
    registros_procesados = models.IntegerField(default=0)
    registros_exitosos = models.IntegerField(default=0)
    registros_fallidos = models.IntegerField(default=0)
    registros_ignorados = models.IntegerField(default=0)
    
    # Detalles
    datos_transferidos_mb = models.FloatField(default=0.0)
    duracion_segundos = models.FloatField(default=0.0)
    
    # Resultado
    fue_exitosa = models.BooleanField(default=True)
    mensaje = models.TextField(blank=True, null=True)
    
    # Timestamps
    timestamp_inicio = models.DateTimeField(auto_now_add=True)
    timestamp_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'registros_sincronizacion'
        verbose_name = _('Registro Sincronización')
        verbose_name_plural = _('Registros Sincronización')
        indexes = [
            models.Index(fields=['sincronizacion', 'timestamp_inicio']),
            models.Index(fields=['timestamp_inicio']),
        ]

    def __str__(self):
        return f"Sync {self.tipo_sincronizacion} - {self.timestamp_inicio}"


class ControlVersionesDB(models.Model):
    """
    Control de versiones de la base de datos local en dispositivos móviles.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey('autenticacion.Usuarios', on_delete=models.CASCADE)
    
    # Versión
    numero_version = models.CharField(max_length=20)
    
    # Cambios
    descripcion_cambios = models.TextField()
    hash_schema = models.CharField(max_length=256)
    
    # Fecha
    fecha_liberacion = models.DateTimeField()
    es_obligatoria = models.BooleanField(default=False)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'control_versiones_db'
        verbose_name = _('Control Versiones DB')
        verbose_name_plural = _('Controles Versiones DB')

    def __str__(self):
        return f"v{self.numero_version} - {self.fecha_liberacion}"
