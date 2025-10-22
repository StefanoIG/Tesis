from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class Usuarios(AbstractUser):
    """
    Modelo personalizado de Usuario basado en AbstractUser.
    Extiende el modelo de usuario de Django con campos adicionales.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    # Relacionales con related_name único
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='usuarios_personalizados'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='usuarios_personalizados'
    )

    class Meta:
        db_table = 'usuarios'
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"


class Roles(models.Model):
    """
    Roles del sistema para control de acceso basado en roles (RBAC).
    Ejemplos: Productor, AdminAsociacion, OperadorPlanta, GerenteCalidad, 
    GerenteLogistica, AdminSistema, Auditor
    """
    ROLE_CHOICES = [
        ('PRODUCTOR', 'Productor'),
        ('ADMIN_ASOCIACION', 'Administrador Asociación'),
        ('OPERADOR_PLANTA', 'Operador Planta'),
        ('GERENTE_CALIDAD', 'Gerente de Calidad'),
        ('GERENTE_LOGISTICA', 'Gerente Logística'),
        ('ADMIN_SISTEMA', 'Administrador Sistema'),
        ('AUDITOR', 'Auditor'),
    ]

    id = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'roles'
        verbose_name = _('Rol')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.nombre_rol


class UsuariosRoles(models.Model):
    """
    Tabla de unión para implementar RBAC (Control de Acceso Basado en Roles).
    Vincula usuarios con roles específicos.
    """
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='roles')
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='usuarios')
    asignado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios_roles'
        verbose_name = _('Usuario Rol')
        verbose_name_plural = _('Usuarios Roles')
        unique_together = ('usuario', 'rol')

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.rol.nombre_rol}"


class Auditorias(models.Model):
    """
    Log de todas las operaciones críticas del sistema para auditoría y cumplimiento normativo.
    """
    RESULTADO_CHOICES = [
        ('EXITOSO', 'Exitoso'),
        ('FALLIDO', 'Fallido'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=100)
    entidad_afectada = models.CharField(max_length=50)
    registro_id = models.UUIDField(null=True, blank=True)
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES, default='EXITOSO')
    mensaje_error = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'auditorias'
        verbose_name = _('Auditoría')
        verbose_name_plural = _('Auditorías')
        indexes = [
            models.Index(fields=['usuario', 'timestamp']),
            models.Index(fields=['entidad_afectada', 'registro_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.accion} - {self.entidad_afectada} - {self.timestamp}"
