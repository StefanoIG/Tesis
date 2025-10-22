from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class ReglasAlertas(models.Model):
    """
    Define reglas para generar alertas automáticas en el sistema.
    """
    OPERADORES_CONDICION = [
        ('IGUAL', '='),
        ('NO_IGUAL', '!='),
        ('MAYOR_QUE', '>'),
        ('MENOR_QUE', '<'),
        ('MAYOR_IGUAL', '>='),
        ('MENOR_IGUAL', '<='),
        ('CONTIENE', 'Contiene'),
    ]

    SEVERIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    
    # Configuración de la regla
    es_activa = models.BooleanField(default=True)
    tipo_alerta = models.CharField(max_length=100, help_text="Ej: Temperatura Anómala, Retraso en Entrega")
    
    # Condición
    campo_monitoreado = models.CharField(max_length=100, help_text="Campo del modelo a monitorear")
    operador = models.CharField(max_length=20, choices=OPERADORES_CONDICION)
    valor_comparacion = models.CharField(max_length=255)
    
    # Severidad
    severidad = models.CharField(max_length=20, choices=SEVERIDADES, default='MEDIA')
    
    # Acciones
    notificar_roles = models.JSONField(default=list, blank=True, help_text="Lista de IDs de roles a notificar")
    notificar_usuarios = models.JSONField(default=list, blank=True, help_text="Lista de IDs de usuarios a notificar")
    
    # Control
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reglas_alertas'
        verbose_name = _('Regla Alerta')
        verbose_name_plural = _('Reglas Alertas')

    def __str__(self):
        return self.nombre


class Alertas(models.Model):
    """
    Alertas generadas en el sistema.
    """
    ESTADOS_ALERTA = [
        ('ABIERTA', 'Abierta'),
        ('RECONOCIDA', 'Reconocida'),
        ('RESUELTA', 'Resuelta'),
        ('FALSA_ALARMA', 'Falsa Alarma'),
    ]

    SEVERIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    regla = models.ForeignKey(ReglasAlertas, on_delete=models.PROTECT)
    
    # Origen de la alerta
    lote = models.ForeignKey(
        'trazabilidad.Lotes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alertas_generales'
    )
    envio = models.ForeignKey(
        'logistica.Envios',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alertas_generales'
    )
    
    # Detalles
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    valor_actual = models.CharField(max_length=255)
    valor_umbral = models.CharField(max_length=255)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADOS_ALERTA, default='ABIERTA')
    severidad = models.CharField(max_length=20, choices=SEVERIDADES)
    
    # Responsable
    usuario_asignado = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alertas_asignadas'
    )
    
    # Resolución
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    comentario_resolucion = models.TextField(blank=True, null=True)
    accion_tomada = models.TextField(blank=True, null=True)
    
    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'alertas'
        verbose_name = _('Alerta')
        verbose_name_plural = _('Alertas')
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['severidad']),
            models.Index(fields=['creado_en']),
            models.Index(fields=['usuario_asignado']),
        ]

    def __str__(self):
        return self.titulo
