from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class DispositivosSensores(models.Model):
    """
    Dispositivos de sensores IoT para monitoreo de condiciones.
    """
    TIPOS_DISPOSITIVO = [
        ('TEMPERATURA', 'Sensor de Temperatura'),
        ('HUMEDAD', 'Sensor de Humedad'),
        ('TEMPERATURA_HUMEDAD', 'Sensor de Temperatura y Humedad'),
        ('PH', 'Sensor de pH'),
        ('LUMINOSIDAD', 'Sensor de Luminosidad'),
        ('HUMEDAD_SUELO', 'Sensor de Humedad de Suelo'),
        ('PLUVIOMETRO', 'Pluviómetro'),
        ('ESTACION_METEOROLOGICA', 'Estación Meteorológica'),
        ('GPS', 'GPS Tracker'),
        ('OTRO', 'Otro'),
    ]

    ESTADOS_DISPOSITIVO = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('AVERIADO', 'Averiado'),
        ('DESINSTALADO', 'Desinstalado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Identificación
    codigo_dispositivo = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=100)
    tipo_dispositivo = models.CharField(max_length=30, choices=TIPOS_DISPOSITIVO)
    
    # Ubicación
    empresa = models.ForeignKey(
        'usuarios.Empresas',
        on_delete=models.CASCADE,
        related_name='sensores',
        null=True,
        blank=True
    )
    finca = models.ForeignKey(
        'usuarios.Fincas',
        on_delete=models.CASCADE,
        related_name='sensores',
        null=True,
        blank=True
    )
    ubicacion = models.ForeignKey(
        'logistica.Ubicaciones',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores'
    )
    
    # Geolocalización
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    descripcion_ubicacion = models.CharField(max_length=255, blank=True, null=True)
    
    # Información técnica
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True)
    firmware_version = models.CharField(max_length=50, blank=True, null=True)
    
    # Configuración
    frecuencia_lectura_minutos = models.IntegerField(
        default=15,
        help_text="Frecuencia de lectura en minutos"
    )
    umbral_alerta_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor mínimo para generar alerta"
    )
    umbral_alerta_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor máximo para generar alerta"
    )
    
    # Estado y mantenimiento
    estado = models.CharField(max_length=20, choices=ESTADOS_DISPOSITIVO, default='ACTIVO')
    fecha_instalacion = models.DateField(null=True, blank=True)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True)
    ultima_lectura_fecha = models.DateTimeField(null=True, blank=True)
    
    # Conectividad
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    
    # Metadata
    configuracion_adicional = models.JSONField(default=dict, blank=True)
    notas = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dispositivos_sensores'
        verbose_name = _('Dispositivo Sensor')
        verbose_name_plural = _('Dispositivos Sensores')
        ordering = ['empresa', 'nombre']
        indexes = [
            models.Index(fields=['codigo_dispositivo']),
            models.Index(fields=['empresa', 'estado']),
            models.Index(fields=['tipo_dispositivo']),
        ]

    def __str__(self):
        return f"{self.codigo_dispositivo} - {self.nombre}"


class LecturasSensores(models.Model):
    """
    Lecturas registradas por los sensores (automáticas o manuales).
    """
    FUENTES_LECTURA = [
        ('AUTOMATICA', 'Lectura Automática'),
        ('MANUAL', 'Lectura Manual'),
        ('IMPORTADA', 'Importada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Dispositivo (opcional para lecturas manuales)
    dispositivo = models.ForeignKey(
        DispositivosSensores,
        on_delete=models.CASCADE,
        related_name='lecturas',
        null=True,
        blank=True
    )
    
    # Relación con entidades
    lote = models.ForeignKey(
        'trazabilidad.Lotes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lecturas_sensores'
    )
    transporte = models.ForeignKey(
        'logistica.Transportes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lecturas_sensores'
    )
    ubicacion = models.ForeignKey(
        'logistica.Ubicaciones',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Datos de la lectura
    tipo_medicion = models.CharField(
        max_length=30,
        help_text="temperatura, humedad, ph, etc."
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20, help_text="°C, %, pH, lux, etc.")
    
    # Metadata de la lectura
    fecha_lectura = models.DateTimeField(db_index=True)
    fuente = models.CharField(max_length=20, choices=FUENTES_LECTURA, default='AUTOMATICA')
    
    # Geolocalización (para lecturas móviles)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Usuario (para lecturas manuales)
    registrado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lecturas_manuales'
    )
    
    # Alertas
    alerta_generada = models.BooleanField(default=False)
    fuera_de_rango = models.BooleanField(default=False)
    
    # Datos adicionales
    datos_adicionales = models.JSONField(default=dict, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lecturas_sensores'
        verbose_name = _('Lectura de Sensor')
        verbose_name_plural = _('Lecturas de Sensores')
        ordering = ['-fecha_lectura']
        indexes = [
            models.Index(fields=['dispositivo', 'fecha_lectura']),
            models.Index(fields=['lote', 'fecha_lectura']),
            models.Index(fields=['transporte', 'fecha_lectura']),
            models.Index(fields=['fecha_lectura']),
            models.Index(fields=['alerta_generada']),
            models.Index(fields=['tipo_medicion']),
        ]

    def __str__(self):
        dispositivo_str = self.dispositivo.codigo_dispositivo if self.dispositivo else 'Manual'
        return f"{dispositivo_str} - {self.tipo_medicion}: {self.valor}{self.unidad_medida}"


class ConfiguracionesAlertasSensor(models.Model):
    """
    Configuración de alertas personalizadas para sensores.
    """
    TIPOS_CONDICION = [
        ('MAYOR_QUE', 'Mayor que'),
        ('MENOR_QUE', 'Menor que'),
        ('IGUAL_A', 'Igual a'),
        ('ENTRE', 'Entre rango'),
        ('FUERA_DE_RANGO', 'Fuera de rango'),
    ]

    NIVELES_ALERTA = [
        ('INFORMATIVA', 'Informativa'),
        ('ADVERTENCIA', 'Advertencia'),
        ('CRITICA', 'Crítica'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Alcance
    dispositivo = models.ForeignKey(
        DispositivosSensores,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='configuraciones_alerta'
    )
    empresa = models.ForeignKey(
        'usuarios.Empresas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Alerta a nivel empresa (todos sus sensores)"
    )
    tipo_medicion = models.CharField(max_length=30)
    
    # Condición
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo_condicion = models.CharField(max_length=20, choices=TIPOS_CONDICION)
    valor_referencia = models.DecimalField(max_digits=10, decimal_places=2)
    valor_referencia_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Para condiciones de rango"
    )
    
    # Configuración de la alerta
    nivel_alerta = models.CharField(max_length=20, choices=NIVELES_ALERTA)
    mensaje_alerta = models.TextField()
    enviar_notificacion = models.BooleanField(default=True)
    
    # Destinatarios
    usuarios_notificar = models.ManyToManyField(
        'autenticacion.Usuarios',
        blank=True,
        related_name='configuraciones_alertas_sensor'
    )
    
    # Control
    es_activa = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'configuraciones_alertas_sensor'
        verbose_name = _('Configuración de Alerta de Sensor')
        verbose_name_plural = _('Configuraciones de Alertas de Sensores')
        ordering = ['nivel_alerta', 'nombre']

    def __str__(self):
        return f"{self.nombre} - {self.nivel_alerta}"

    def evaluar_lectura(self, valor):
        """Evalúa si una lectura debe generar alerta."""
        if self.tipo_condicion == 'MAYOR_QUE':
            return valor > self.valor_referencia
        elif self.tipo_condicion == 'MENOR_QUE':
            return valor < self.valor_referencia
        elif self.tipo_condicion == 'IGUAL_A':
            return valor == self.valor_referencia
        elif self.tipo_condicion == 'ENTRE':
            return self.valor_referencia <= valor <= self.valor_referencia_max
        elif self.tipo_condicion == 'FUERA_DE_RANGO':
            return valor < self.valor_referencia or valor > self.valor_referencia_max
        return False


class RegistrosMantenimientoSensor(models.Model):
    """
    Registro de mantenimientos realizados a los sensores.
    """
    TIPOS_MANTENIMIENTO = [
        ('PREVENTIVO', 'Mantenimiento Preventivo'),
        ('CORRECTIVO', 'Mantenimiento Correctivo'),
        ('CALIBRACION', 'Calibración'),
        ('ACTUALIZACION_FIRMWARE', 'Actualización de Firmware'),
        ('REEMPLAZO', 'Reemplazo'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dispositivo = models.ForeignKey(
        DispositivosSensores,
        on_delete=models.CASCADE,
        related_name='mantenimientos'
    )
    
    # Información del mantenimiento
    tipo_mantenimiento = models.CharField(max_length=30, choices=TIPOS_MANTENIMIENTO)
    fecha_mantenimiento = models.DateField()
    descripcion = models.TextField()
    
    # Técnico
    tecnico_nombre = models.CharField(max_length=100)
    tecnico_empresa = models.CharField(max_length=100, blank=True, null=True)
    
    # Costos
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Resultado
    resultado = models.TextField(blank=True, null=True)
    repuestos_utilizados = models.JSONField(default=list, blank=True)
    
    # Próximo mantenimiento
    proximo_mantenimiento = models.DateField(null=True, blank=True)
    
    # Usuario que registra
    registrado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registros_mantenimiento_sensor'
        verbose_name = _('Registro de Mantenimiento de Sensor')
        verbose_name_plural = _('Registros de Mantenimiento de Sensores')
        ordering = ['-fecha_mantenimiento']
        indexes = [
            models.Index(fields=['dispositivo', 'fecha_mantenimiento']),
        ]

    def __str__(self):
        return f"{self.dispositivo.codigo_dispositivo} - {self.tipo_mantenimiento} - {self.fecha_mantenimiento}"
