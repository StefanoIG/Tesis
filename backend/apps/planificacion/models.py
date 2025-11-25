from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class EstudiosSuelo(models.Model):
    """
    Estudios de suelo realizados en fincas o parcelas.
    Pueden ser cargados como PDF o ingresados manualmente.
    """
    TIPOS_TEXTURA = [
        ('ARENOSO', 'Arenoso'),
        ('LIMOSO', 'Limoso'),
        ('ARCILLOSO', 'Arcilloso'),
        ('FRANCO', 'Franco'),
        ('FRANCO_ARENOSO', 'Franco Arenoso'),
        ('FRANCO_ARCILLOSO', 'Franco Arcilloso'),
        ('FRANCO_LIMOSO', 'Franco Limoso'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    finca = models.ForeignKey(
        'usuarios.Fincas',
        on_delete=models.CASCADE,
        related_name='estudios_suelo'
    )
    parcela = models.ForeignKey(
        'Parcelas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='estudios_suelo'
    )
    
    # Información básica
    nombre = models.CharField(max_length=255)
    fecha_estudio = models.DateField()
    laboratorio = models.CharField(max_length=255, blank=True, null=True)
    
    # Documento
    archivo_pdf = models.FileField(
        upload_to='estudios_suelo/',
        null=True,
        blank=True,
        help_text="PDF del estudio de suelo"
    )
    
    # Datos del suelo
    ph = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(14)],
        null=True,
        blank=True
    )
    textura = models.CharField(max_length=30, choices=TIPOS_TEXTURA, blank=True, null=True)
    
    # Nutrientes (en ppm o mg/kg)
    nitrogeno = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="N en ppm")
    fosforo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="P en ppm")
    potasio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="K in ppm")
    calcio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    magnesio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    azufre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Micronutrientes
    hierro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    manganeso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    zinc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cobre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    boro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Propiedades físicas
    materia_organica = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Porcentaje"
    )
    conductividad_electrica = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="dS/m"
    )
    capacidad_intercambio_cationico = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="meq/100g"
    )
    
    # Análisis y recomendaciones
    observaciones = models.TextField(blank=True, null=True)
    recomendaciones_laboratorio = models.TextField(blank=True, null=True)
    
    # Metadata
    datos_adicionales = models.JSONField(default=dict, blank=True)
    es_vigente = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estudios_suelo'
        verbose_name = _('Estudio de Suelo')
        verbose_name_plural = _('Estudios de Suelo')
        ordering = ['-fecha_estudio']

    def __str__(self):
        return f"{self.nombre} - {self.finca.nombre} ({self.fecha_estudio})"


class Parcelas(models.Model):
    """
    Subdivisiones de una finca para mejor gestión.
    Pueden tener geometría SVG para visualización en mapa.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    finca = models.ForeignKey(
        'usuarios.Fincas',
        on_delete=models.CASCADE,
        related_name='parcelas'
    )
    
    # Información básica
    codigo_parcela = models.CharField(max_length=50, db_index=True)
    nombre = models.CharField(max_length=255)
    area_hectareas = models.DecimalField(max_digits=10, decimal_places=4)
    
    # Geometría y ubicación
    geometria_svg = models.TextField(
        blank=True,
        null=True,
        help_text="Datos SVG para dibujar la parcela en el mapa"
    )
    coordenadas_geojson = models.JSONField(
        default=dict,
        blank=True,
        help_text="GeoJSON con las coordenadas de la parcela"
    )
    
    # Coordenadas centrales
    latitud_centro = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud_centro = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Estado actual
    cultivo_actual = models.ForeignKey(
        'CatalogosCultivos',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parcelas_actuales'
    )
    fecha_siembra_actual = models.DateField(null=True, blank=True)
    estado_parcela = models.CharField(
        max_length=30,
        choices=[
            ('DISPONIBLE', 'Disponible'),
            ('EN_USO', 'En Uso'),
            ('DESCANSO', 'En Descanso'),
            ('PREPARACION', 'En Preparación'),
            ('INACTIVA', 'Inactiva'),
        ],
        default='DISPONIBLE'
    )
    
    # Metadata
    observaciones = models.TextField(blank=True, null=True)
    es_activa = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parcelas'
        verbose_name = _('Parcela')
        verbose_name_plural = _('Parcelas')
        unique_together = ('finca', 'codigo_parcela')
        ordering = ['finca', 'codigo_parcela']

    def __str__(self):
        return f"{self.finca.nombre} - {self.nombre} ({self.codigo_parcela})"


class CatalogosCultivos(models.Model):
    """
    Catálogo de cultivos disponibles con sus características y requisitos.
    """
    CATEGORIAS_CULTIVO = [
        ('FLORES', 'Flores'),
        ('FRUTAS', 'Frutas'),
        ('HORTALIZAS', 'Hortalizas'),
        ('GRANOS', 'Granos'),
        ('TUBERCULOS', 'Tubérculos'),
        ('ESPECIAS', 'Especias y Hierbas'),
        ('FORRAJES', 'Forrajes'),
        ('OTROS', 'Otros'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Información básica
    nombre_cientifico = models.CharField(max_length=255)
    nombre_comun = models.CharField(max_length=255, unique=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS_CULTIVO)
    variedades = models.JSONField(default=list, blank=True, help_text="Lista de variedades disponibles")
    
    # Requisitos de suelo
    ph_minimo = models.DecimalField(max_digits=3, decimal_places=1, default=5.5)
    ph_optimo_min = models.DecimalField(max_digits=3, decimal_places=1, default=6.0)
    ph_optimo_max = models.DecimalField(max_digits=3, decimal_places=1, default=7.0)
    ph_maximo = models.DecimalField(max_digits=3, decimal_places=1, default=8.0)
    
    texturas_compatibles = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de texturas de suelo compatibles"
    )
    
    # Requisitos climáticos
    temperatura_min = models.DecimalField(max_digits=4, decimal_places=1, help_text="°C")
    temperatura_optima_min = models.DecimalField(max_digits=4, decimal_places=1, help_text="°C")
    temperatura_optima_max = models.DecimalField(max_digits=4, decimal_places=1, help_text="°C")
    temperatura_max = models.DecimalField(max_digits=4, decimal_places=1, help_text="°C")
    
    altitud_minima = models.IntegerField(default=0, help_text="metros sobre el nivel del mar")
    altitud_maxima = models.IntegerField(default=5000, help_text="metros sobre el nivel del mar")
    
    precipitacion_anual_min = models.IntegerField(help_text="mm/año")
    precipitacion_anual_max = models.IntegerField(help_text="mm/año")
    
    # Ciclo de cultivo
    dias_germinacion = models.IntegerField(default=0)
    dias_hasta_cosecha = models.IntegerField(help_text="Días desde siembra")
    ciclos_por_anio = models.IntegerField(default=1)
    
    # Requerimientos de riego
    frecuencia_riego_dias = models.IntegerField(
        default=7,
        help_text="Frecuencia recomendada de riego en días (sin sensores)"
    )
    litros_agua_por_planta_dia = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    requiere_riego_constante = models.BooleanField(default=False)
    
    # Rentabilidad y mercado
    rendimiento_promedio_hectarea = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Toneladas o unidades por hectárea"
    )
    precio_mercado_promedio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="USD por kg o unidad"
    )
    demanda_mercado = models.CharField(
        max_length=20,
        choices=[
            ('MUY_ALTA', 'Muy Alta'),
            ('ALTA', 'Alta'),
            ('MEDIA', 'Media'),
            ('BAJA', 'Baja'),
        ],
        default='MEDIA'
    )
    
    # Dificultad
    nivel_dificultad = models.CharField(
        max_length=20,
        choices=[
            ('FACIL', 'Fácil'),
            ('MODERADO', 'Moderado'),
            ('DIFICIL', 'Difícil'),
            ('EXPERTO', 'Experto'),
        ],
        default='MODERADO'
    )
    
    # Certificaciones y permisos
    certificaciones_recomendadas = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de certificaciones relevantes"
    )
    permisos_requeridos_ecuador = models.JSONField(
        default=list,
        blank=True,
        help_text="Permisos AGROCALIDAD, MAG, etc."
    )
    
    # Información adicional
    descripcion = models.TextField(blank=True, null=True)
    plagas_comunes = models.JSONField(default=list, blank=True)
    enfermedades_comunes = models.JSONField(default=list, blank=True)
    compatibilidad_rotacion = models.JSONField(
        default=list,
        blank=True,
        help_text="Cultivos compatibles para rotación"
    )
    
    # Control
    es_activo = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalogos_cultivos'
        verbose_name = _('Catálogo de Cultivo')
        verbose_name_plural = _('Catálogos de Cultivos')
        ordering = ['categoria', 'nombre_comun']

    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"


class PlanesCultivo(models.Model):
    """
    Planificación de cultivos para una parcela específica.
    """
    ESTADOS_PLAN = [
        ('PROPUESTA', 'Propuesta'),
        ('APROBADO', 'Aprobado'),
        ('EN_EJECUCION', 'En Ejecución'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parcela = models.ForeignKey(Parcelas, on_delete=models.CASCADE, related_name='planes_cultivo')
    cultivo = models.ForeignKey(CatalogosCultivos, on_delete=models.PROTECT, related_name='planes')
    
    # Planificación
    fecha_planificada_siembra = models.DateField()
    fecha_estimada_cosecha = models.DateField()
    fecha_real_siembra = models.DateField(null=True, blank=True)
    fecha_real_cosecha = models.DateField(null=True, blank=True)
    
    # Detalles
    variedad = models.CharField(max_length=100, blank=True, null=True)
    cantidad_plantas = models.IntegerField(null=True, blank=True)
    densidad_siembra = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ej: 2x3 metros, 30cm entre plantas"
    )
    
    # Estado y seguimiento
    estado = models.CharField(max_length=20, choices=ESTADOS_PLAN, default='PROPUESTA')
    progreso_porcentaje = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Análisis y recomendaciones
    compatibilidad_suelo = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Porcentaje de compatibilidad basado en estudio de suelo"
    )
    motivo_seleccion = models.TextField(
        blank=True,
        null=True,
        help_text="Por qué se eligió este cultivo"
    )
    recomendaciones_ia = models.JSONField(
        default=dict,
        blank=True,
        help_text="Recomendaciones generadas por el sistema"
    )
    
    # Costos y proyección
    inversion_estimada = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ingreso_proyectado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    roi_estimado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Retorno de inversión en porcentaje"
    )
    
    # Control
    creado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        related_name='planes_cultivo_creados'
    )
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'planes_cultivo'
        verbose_name = _('Plan de Cultivo')
        verbose_name_plural = _('Planes de Cultivo')
        ordering = ['-fecha_planificada_siembra']

    def __str__(self):
        return f"{self.parcela.nombre} - {self.cultivo.nombre_comun} ({self.fecha_planificada_siembra})"


class CalendariosRiego(models.Model):
    """
    Calendarios y programación de riego para parcelas.
    Se genera automáticamente con sensores o manualmente sin ellos.
    """
    TIPOS_RIEGO = [
        ('GOTEO', 'Goteo'),
        ('ASPERSION', 'Aspersión'),
        ('GRAVEDAD', 'Gravedad'),
        ('MICROASPERSION', 'Microaspersión'),
        ('MANUAL', 'Manual'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_cultivo = models.ForeignKey(
        PlanesCultivo,
        on_delete=models.CASCADE,
        related_name='calendarios_riego'
    )
    
    # Configuración
    tipo_riego = models.CharField(max_length=30, choices=TIPOS_RIEGO)
    frecuencia_dias = models.IntegerField(help_text="Cada cuántos días regar")
    duracion_minutos = models.IntegerField(help_text="Duración del riego en minutos")
    litros_por_riego = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Horarios
    hora_inicio_recomendada = models.TimeField(help_text="Hora recomendada para regar")
    dias_semana = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de días de la semana [0=Lunes, 6=Domingo]"
    )
    
    # Ajustes por clima
    ajustar_por_lluvia = models.BooleanField(default=True)
    ajustar_por_temperatura = models.BooleanField(default=False)
    
    # Control automático con sensores
    usa_sensores = models.BooleanField(default=False)
    sensor_humedad = models.ForeignKey(
        'sensores.DispositivosSensores',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calendarios_riego'
    )
    umbral_humedad_minimo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Porcentaje mínimo de humedad para activar riego"
    )
    umbral_humedad_maximo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Porcentaje máximo de humedad para detener riego"
    )
    
    # Estado
    es_activo = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'calendarios_riego'
        verbose_name = _('Calendario de Riego')
        verbose_name_plural = _('Calendarios de Riego')

    def __str__(self):
        return f"Riego {self.plan_cultivo.parcela.nombre} - Cada {self.frecuencia_dias} días"


class RegistrosRiego(models.Model):
    """
    Registro de riegos ejecutados (automáticos o manuales).
    """
    TIPOS_EJECUCION = [
        ('AUTOMATICO', 'Automático (sensor)'),
        ('PROGRAMADO', 'Programado (calendario)'),
        ('MANUAL', 'Manual'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calendario = models.ForeignKey(
        CalendariosRiego,
        on_delete=models.CASCADE,
        related_name='registros_ejecucion'
    )
    
    # Detalles del riego
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(null=True, blank=True)
    duracion_real_minutos = models.IntegerField(null=True, blank=True)
    litros_agua_utilizados = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Tipo de ejecución
    tipo_ejecucion = models.CharField(max_length=20, choices=TIPOS_EJECUCION)
    ejecutado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Condiciones al momento del riego
    temperatura_ambiente = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    humedad_suelo_antes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humedad_suelo_despues = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    incidencias = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registros_riego'
        verbose_name = _('Registro de Riego')
        verbose_name_plural = _('Registros de Riego')
        ordering = ['-fecha_hora_inicio']

    def __str__(self):
        return f"Riego {self.calendario.plan_cultivo.parcela.nombre} - {self.fecha_hora_inicio}"


class PermisosNacionalesEcuador(models.Model):
    """
    Catálogo de permisos nacionales requeridos en Ecuador para actividades agrícolas.
    """
    ENTIDADES_EMISORAS = [
        ('AGROCALIDAD', 'AGROCALIDAD'),
        ('MAG', 'Ministerio de Agricultura y Ganadería'),
        ('MAATE', 'Ministerio del Ambiente'),
        ('ARCSA', 'ARCSA'),
        ('SENADI', 'SENADI (para exportación)'),
        ('GAD_MUNICIPAL', 'GAD Municipal'),
        ('GAD_PROVINCIAL', 'GAD Provincial'),
        ('OTRO', 'Otro'),
    ]

    TIPOS_PERMISO = [
        ('FITOSANITARIO', 'Fitosanitario'),
        ('AMBIENTAL', 'Ambiental'),
        ('USO_AGUA', 'Uso de Agua'),
        ('EXPORTACION', 'Exportación'),
        ('IMPORTACION', 'Importación'),
        ('PRODUCCION', 'Producción'),
        ('COMERCIALIZACION', 'Comercialización'),
        ('TRANSPORTE', 'Transporte'),
        ('OTRO', 'Otro'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Información del permiso
    nombre_permiso = models.CharField(max_length=255)
    codigo_permiso = models.CharField(max_length=100, unique=True)
    tipo_permiso = models.CharField(max_length=30, choices=TIPOS_PERMISO)
    entidad_emisora = models.CharField(max_length=30, choices=ENTIDADES_EMISORAS)
    
    # Descripción y requisitos
    descripcion = models.TextField()
    requisitos = models.JSONField(
        default=list,
        help_text="Lista de requisitos necesarios"
    )
    documentos_requeridos = models.JSONField(
        default=list,
        help_text="Lista de documentos requeridos"
    )
    
    # Aplicabilidad
    cultivos_aplicables = models.ManyToManyField(
        CatalogosCultivos,
        blank=True,
        related_name='permisos_requeridos'
    )
    aplica_todo_cultivo = models.BooleanField(default=False)
    
    # Trámite
    tiempo_tramite_dias = models.IntegerField(help_text="Días estimados para obtener el permiso")
    vigencia_meses = models.IntegerField(help_text="Meses de vigencia del permiso")
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Enlaces útiles
    url_tramite = models.URLField(blank=True, null=True)
    url_informacion = models.URLField(blank=True, null=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    es_obligatorio = models.BooleanField(default=True)
    es_activo = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permisos_nacionales_ecuador'
        verbose_name = _('Permiso Nacional Ecuador')
        verbose_name_plural = _('Permisos Nacionales Ecuador')
        ordering = ['entidad_emisora', 'nombre_permiso']

    def __str__(self):
        return f"{self.codigo_permiso} - {self.nombre_permiso} ({self.entidad_emisora})"


class PermisosObtenidos(models.Model):
    """
    Registro de permisos obtenidos por empresas/fincas.
    """
    ESTADOS_PERMISO = [
        ('EN_TRAMITE', 'En Trámite'),
        ('VIGENTE', 'Vigente'),
        ('POR_RENOVAR', 'Por Renovar'),
        ('VENCIDO', 'Vencido'),
        ('RECHAZADO', 'Rechazado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permiso = models.ForeignKey(
        PermisosNacionalesEcuador,
        on_delete=models.PROTECT,
        related_name='permisos_obtenidos'
    )
    empresa = models.ForeignKey(
        'usuarios.Empresas',
        on_delete=models.CASCADE,
        related_name='permisos_obtenidos'
    )
    finca = models.ForeignKey(
        'usuarios.Fincas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='permisos_obtenidos'
    )
    
    # Información del permiso obtenido
    numero_permiso = models.CharField(max_length=100, unique=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS_PERMISO, default='EN_TRAMITE')
    
    # Documentos
    archivo_permiso = models.FileField(
        upload_to='permisos/',
        null=True,
        blank=True
    )
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permisos_obtenidos'
        verbose_name = _('Permiso Obtenido')
        verbose_name_plural = _('Permisos Obtenidos')
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"{self.permiso.nombre_permiso} - {self.empresa.nombre} ({self.numero_permiso})"
