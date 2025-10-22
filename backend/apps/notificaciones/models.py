from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Notificaciones(models.Model):
    """
    Notificaciones para usuarios del sistema.
    Sistema de pulling: el cliente consulta periódicamente las notificaciones no leídas.
    """
    TIPOS_NOTIFICACION = [
        ('ALERTA', 'Alerta'),
        ('EVENTO_TRAZABILIDAD', 'Evento Trazabilidad'),
        ('ENVIO_ESTADO', 'Estado de Envío'),
        ('CALIDAD', 'Control de Calidad'),
        ('SINCRONIZACION', 'Sincronización'),
        ('SISTEMA', 'Sistema'),
        ('INFORMATIVO', 'Informativo'),
    ]

    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario_destinatario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    
    # Contenido
    tipo_notificacion = models.CharField(max_length=50, choices=TIPOS_NOTIFICACION)
    titulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='MEDIA')
    
    # Referencias
    alerta = models.ForeignKey(
        'alertas.Alertas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notificaciones'
    )
    evento_trazabilidad = models.ForeignKey(
        'trazabilidad.EventosTrazabilidad',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notificaciones'
    )
    envio = models.ForeignKey(
        'logistica.Envios',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notificaciones'
    )
    lote = models.ForeignKey(
        'trazabilidad.Lotes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notificaciones'
    )
    
    # Data adicional (json para información contextual)
    datos_adicionales = models.JSONField(default=dict, blank=True)
    
    # Control de lectura
    fue_leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    
    # Control de expiración
    fecha_expiracion = models.DateTimeField(null=True, blank=True, help_text="Fecha en que la notificación se elimina")
    
    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notificaciones'
        verbose_name = _('Notificación')
        verbose_name_plural = _('Notificaciones')
        indexes = [
            models.Index(fields=['usuario_destinatario', 'fue_leida', 'creado_en']),
            models.Index(fields=['fue_leida']),
            models.Index(fields=['prioridad']),
            models.Index(fields=['creado_en']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.usuario_destinatario.email}"


class PreferenciasNotificaciones(models.Model):
    """
    Preferencias de notificación por usuario.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(
        'autenticacion.Usuarios',
        on_delete=models.CASCADE,
        related_name='preferencias_notificaciones'
    )
    
    # Tipos de notificaciones habilitadas
    alertas_habilitadas = models.BooleanField(default=True)
    eventos_trazabilidad_habilitados = models.BooleanField(default=True)
    estados_envios_habilitados = models.BooleanField(default=True)
    calidad_habilitada = models.BooleanField(default=True)
    sincronizacion_habilitada = models.BooleanField(default=False)
    sistema_habilitada = models.BooleanField(default=True)
    
    # Configuración de frecuencia
    intervalo_polling_segundos = models.IntegerField(default=300, help_text="Cada cuántos segundos el cliente consulta notificaciones")
    eliminar_notificaciones_leidas_dias = models.IntegerField(default=30)
    
    # Horarios silenciosos (opcional)
    silencioso_horario_inicio = models.TimeField(null=True, blank=True, help_text="Hora de inicio (HH:MM)")
    silencioso_horario_fin = models.TimeField(null=True, blank=True, help_text="Hora de fin (HH:MM)")
    
    # Auditoría
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'preferencias_notificaciones'
        verbose_name = _('Preferencias Notificaciones')
        verbose_name_plural = _('Preferencias Notificaciones')

    def __str__(self):
        return f"Preferencias - {self.usuario.email}"


class HistorialLecturaNotifc(models.Model):
    """
    Historial de lectura de notificaciones.
    Permite auditar cuándo y dónde fueron leídas las notificaciones.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notificacion = models.ForeignKey(
        Notificaciones,
        on_delete=models.CASCADE,
        related_name='historial_lectura'
    )
    
    # Información del dispositivo
    tipo_dispositivo = models.CharField(
        max_length=20,
        choices=[('ANDROID', 'Android'), ('IOS', 'iOS'), ('WEB', 'Web'), ('API', 'API REST')]
    )
    codigo_dispositivo = models.CharField(max_length=100, null=True, blank=True)
    
    # Lectura
    timestamp_lectura = models.DateTimeField(auto_now_add=True)
    ip_dispositivo = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'historial_lectura_notificaciones'
        verbose_name = _('Historial Lectura Notificación')
        verbose_name_plural = _('Historiales Lectura Notificaciones')

    def __str__(self):
        return f"Lectura - {self.notificacion.titulo} - {self.timestamp_lectura}"
