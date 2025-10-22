from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Empresas(models.Model):
    """
    Organizaciones que participan en la cadena agroindustrial.
    """
    TIPOS_EMPRESA = [
        ('PRODUCTOR', 'Productor Agrícola'),
        ('ACOPIO', 'Centro de Acopio'),
        ('TRANSFORMACION', 'Empresa de Transformación'),
        ('EXPORTADOR', 'Empresa Exportadora'),
        ('DISTRIBUIDOR', 'Distribuidor'),
        ('ASOCIACION', 'Asociación Productiva'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255, unique=True)
    tipo_empresa = models.CharField(max_length=50, choices=TIPOS_EMPRESA)
    registro_nacional = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    # Información de contacto
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='Ecuador')
    
    # Información operativa
    es_activa = models.BooleanField(default=True)
    certificaciones = models.JSONField(default=list, blank=True, help_text="Lista de certificaciones (GlobalG.A.P, AGROCALIDAD, etc)")
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empresas'
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['tipo_empresa']),
        ]

    def __str__(self):
        return self.nombre


class Fincas(models.Model):
    """
    Propiedades o ubicaciones productivas donde se generan los lotes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='fincas')
    nombre = models.CharField(max_length=255)
    codigo_finca = models.CharField(max_length=50, unique=True)
    
    # Localización
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    coordenadas_latitud = models.FloatField()
    coordenadas_longitud = models.FloatField()
    
    # Información operativa
    tamaño_hectareas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    es_activa = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fincas'
        verbose_name = _('Finca')
        verbose_name_plural = _('Fincas')
        unique_together = ('empresa', 'codigo_finca')

    def __str__(self):
        return f"{self.empresa.nombre} - {self.nombre}"


class UsuariosEmpresas(models.Model):
    """
    Vinculación entre usuarios y empresas/fincas.
    Permite que un usuario esté asociado a múltiples empresas.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey('autenticacion.Usuarios', on_delete=models.CASCADE, related_name='empresas')
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='usuarios')
    finca = models.ForeignKey(Fincas, on_delete=models.SET_NULL, null=True, blank=True)
    
    es_responsable = models.BooleanField(default=False, help_text="Si es responsable/gerente de la empresa")
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios_empresas'
        verbose_name = _('Usuario Empresa')
        verbose_name_plural = _('Usuarios Empresas')
        unique_together = ('usuario', 'empresa')

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.empresa.nombre}"


class Permisos(models.Model):
    """
    Permisos granulares para el sistema RBAC.
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    codigo = models.CharField(max_length=50, unique=True, help_text="Ej: crear_lote, editar_evento")

    class Meta:
        db_table = 'permisos'
        verbose_name = _('Permiso')
        verbose_name_plural = _('Permisos')

    def __str__(self):
        return self.nombre


class RolesPermisos(models.Model):
    """
    Asignación de permisos a roles.
    """
    rol = models.ForeignKey('autenticacion.Roles', on_delete=models.CASCADE, related_name='permisos')
    permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE)

    class Meta:
        db_table = 'roles_permisos'
        verbose_name = _('Rol Permiso')
        verbose_name_plural = _('Roles Permisos')
        unique_together = ('rol', 'permiso')

    def __str__(self):
        return f"{self.rol.nombre_rol} - {self.permiso.nombre}"
