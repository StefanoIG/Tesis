from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Vehiculos(models.Model):
    """
    Registro de vehículos utilizados para transporte de lotes.
    """
    TIPOS_VEHICULO = [
        ('CAMION', 'Camión'),
        ('FURGONETA', 'Furgoneta'),
        ('AUTO', 'Automóvil'),
        ('MOTO', 'Motocicleta'),
        ('OTRO', 'Otro'),
    ]

    ESTADOS_VEHICULO = [
        ('DISPONIBLE', 'Disponible'),
        ('EN_TRANSITO', 'En Tránsito'),
        ('EN_MANTENIMIENTO', 'En Mantenimiento'),
        ('FUERA_SERVICIO', 'Fuera de Servicio'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey('usuarios.Empresas', on_delete=models.CASCADE, related_name='vehiculos')
    
    # Información del vehículo
    placa = models.CharField(max_length=20, unique=True)
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPOS_VEHICULO)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año_fabricacion = models.IntegerField()
    
    # Capacidad
    capacidad_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    capacidad_volumen_m3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Características
    es_refrigerado = models.BooleanField(default=False)
    temperatura_min = models.FloatField(null=True, blank=True, help_text="Temperatura mínima en °C")
    temperatura_max = models.FloatField(null=True, blank=True, help_text="Temperatura máxima en °C")
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADOS_VEHICULO, default='DISPONIBLE')
    
    # Documentación
    numero_seguro = models.CharField(max_length=100, blank=True, null=True)
    fecha_vencimiento_seguro = models.DateField(null=True, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vehiculos'
        verbose_name = _('Vehículo')
        verbose_name_plural = _('Vehículos')
        indexes = [
            models.Index(fields=['placa']),
            models.Index(fields=['empresa', 'estado']),
        ]

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"


class Conductores(models.Model):
    """
    Registro de conductores autorizados.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField('autenticacion.Usuarios', on_delete=models.CASCADE)
    
    # Información de licencia
    numero_licencia = models.CharField(max_length=50, unique=True)
    categoria_licencia = models.CharField(max_length=10, default='C')  # A, B, C, D, etc
    fecha_vencimiento_licencia = models.DateField()
    
    # Información adicional
    empresa = models.ForeignKey('usuarios.Empresas', on_delete=models.CASCADE, related_name='conductores')
    es_activo = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conductores'
        verbose_name = _('Conductor')
        verbose_name_plural = _('Conductores')

    def __str__(self):
        return f"{self.usuario.nombre_completo} ({self.numero_licencia})"


class Envios(models.Model):
    """
    Registro de envíos de lotes entre ubicaciones.
    """
    ESTADOS_ENVIO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_TRANSITO', 'En Tránsito'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
        ('DEVUELTO', 'Devuelto'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lote = models.ForeignKey('trazabilidad.Lotes', on_delete=models.CASCADE, related_name='envios')
    
    # Origen y destino
    latitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_origen = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    nombre_origen = models.CharField(max_length=255)
    
    latitud_destino = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_destino = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    nombre_destino = models.CharField(max_length=255)
    
    # Vehículo y conductor (opcionales para crear envio sin asignar)
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.PROTECT, null=True, blank=True)
    conductor = models.ForeignKey(Conductores, on_delete=models.PROTECT, null=True, blank=True)
    
    # Fechas
    fecha_salida = models.DateTimeField(null=True, blank=True)
    fecha_llegada_estimada = models.DateTimeField(null=True, blank=True)
    fecha_llegada_real = models.DateTimeField(null=True, blank=True)
    
    # Control de transporte
    temperatura_registrada = models.FloatField(null=True, blank=True)
    humedad_registrada = models.FloatField(null=True, blank=True)
    distancia_km = models.FloatField(null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADOS_ENVIO, default='PENDIENTE')
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    incidencias = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'envios'
        verbose_name = _('Envío')
        verbose_name_plural = _('Envíos')
        indexes = [
            models.Index(fields=['lote', 'fecha_salida']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_salida']),
        ]

    def __str__(self):
        return f"{self.lote.codigo_lote} - {self.nombre_origen} -> {self.nombre_destino}"


class RuteTrackingActual(models.Model):
    """
    Rastreo en tiempo real de la ubicación de envíos durante el transporte.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envio = models.ForeignKey(Envios, on_delete=models.CASCADE, related_name='tracking')
    
    # Ubicación actual
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Condiciones durante el transporte
    temperatura = models.FloatField(null=True, blank=True)
    humedad = models.FloatField(null=True, blank=True)
    velocidad_kmh = models.FloatField(null=True, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'rute_tracking_actual'
        verbose_name = _('Rastreo de Ruta')
        verbose_name_plural = _('Rastreos de Rutas')
        indexes = [
            models.Index(fields=['envio', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.envio.lote.codigo_lote} - {self.timestamp}"


class AlertasLogistica(models.Model):
    """
    Alertas relacionadas con desviaciones en transporte.
    """
    TIPOS_ALERTA = [
        ('RETRASO', 'Retraso'),
        ('TEMPERATURA', 'Variación de Temperatura'),
        ('DESVIACION_RUTA', 'Desviación de Ruta'),
        ('AVERIA', 'Avería del Vehículo'),
        ('OTRO', 'Otro'),
    ]

    ESTADOS_ALERTA = [
        ('ACTIVA', 'Activa'),
        ('RESUELTA', 'Resuelta'),
        ('CANCELADA', 'Cancelada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envio = models.ForeignKey(Envios, on_delete=models.CASCADE, related_name='alertas')
    
    tipo_alerta = models.CharField(max_length=50, choices=TIPOS_ALERTA)
    estado_alerta = models.CharField(max_length=20, choices=ESTADOS_ALERTA, default='ACTIVA')
    
    descripcion = models.TextField()
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    
    accion_tomada = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'alertas_logistica'
        verbose_name = _('Alerta Logística')
        verbose_name_plural = _('Alertas Logística')

    def __str__(self):
        return f"{self.tipo_alerta} - {self.estado_alerta}"
