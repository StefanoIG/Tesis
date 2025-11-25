from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# NOTA: El modelo Auditorias ya existe en apps.autenticacion
# Por lo tanto, este módulo solo define modelos adicionales de auditoría


class SesionesUsuario(models.Model):
    """
    Registro de sesiones de usuarios para control de acceso.
    """
    ESTADOS_SESION = [
        ('ACTIVA', 'Activa'),
        ('CERRADA', 'Cerrada'),
        ('EXPIRADA', 'Expirada'),
        ('FORZADA_CIERRE', 'Forzada a Cerrar'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.CASCADE,
        related_name='sesiones'
    )
    
    # Información de la sesión
    token_sesion = models.CharField(max_length=255, unique=True)
    ip_origen = models.GenericIPAddressField()
    user_agent = models.TextField()
    dispositivo = models.CharField(max_length=100, blank=True, null=True)
    
    # Geolocalización aproximada
    pais = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    
    # Control de sesión
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actividad = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_SESION, default='ACTIVA')
    
    # Metadata
    metadatos = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'sesiones_usuario'
        verbose_name = _('Sesión de Usuario')
        verbose_name_plural = _('Sesiones de Usuario')
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['usuario', 'estado']),
            models.Index(fields=['token_sesion']),
            models.Index(fields=['fecha_inicio']),
        ]

    def __str__(self):
        return f"{self.usuario.email} - {self.fecha_inicio} - {self.estado}"
