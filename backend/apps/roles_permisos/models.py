from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Roles(models.Model):
    """
    Roles del sistema para implementar RBAC (Control de Acceso Basado en Roles).
    """
    TIPO_ROL = [
        ('SISTEMA', 'Rol del Sistema'),
        ('PERSONALIZADO', 'Rol Personalizado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_rol = models.CharField(max_length=50, unique=True)
    codigo_rol = models.CharField(max_length=30, unique=True, db_index=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_rol = models.CharField(max_length=20, choices=TIPO_ROL, default='PERSONALIZADO')
    
    # Control
    es_activo = models.BooleanField(default=True)
    nivel_acceso = models.IntegerField(
        default=1, 
        help_text="Nivel de acceso jerárquico (1=básico, 10=administrador)"
    )
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles_extendidos'
        verbose_name = _('Rol')
        verbose_name_plural = _('Roles')
        ordering = ['-nivel_acceso', 'nombre_rol']

    def __str__(self):
        return self.nombre_rol


class Permisos(models.Model):
    """
    Permisos granulares del sistema.
    """
    TIPO_PERMISO = [
        ('LECTURA', 'Lectura'),
        ('ESCRITURA', 'Escritura'),
        ('ELIMINACION', 'Eliminación'),
        ('ADMINISTRACION', 'Administración'),
        ('ESPECIAL', 'Especial'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_permiso = models.CharField(max_length=100, unique=True)
    codigo_permiso = models.CharField(max_length=50, unique=True, db_index=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_permiso = models.CharField(max_length=20, choices=TIPO_PERMISO)
    
    # Agrupación
    modulo = models.CharField(max_length=50, help_text="Módulo al que pertenece (usuarios, lotes, etc)")
    recurso = models.CharField(max_length=50, help_text="Recurso específico dentro del módulo")
    
    # Control
    es_activo = models.BooleanField(default=True)
    es_critico = models.BooleanField(
        default=False, 
        help_text="Permiso crítico que requiere mayor control"
    )
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permisos_extendidos'
        verbose_name = _('Permiso')
        verbose_name_plural = _('Permisos')
        ordering = ['modulo', 'recurso', 'tipo_permiso']
        indexes = [
            models.Index(fields=['modulo', 'recurso']),
            models.Index(fields=['codigo_permiso']),
        ]

    def __str__(self):
        return f"{self.modulo}.{self.recurso}.{self.tipo_permiso}"


class RolesPermisos(models.Model):
    """
    Relación muchos a muchos entre Roles y Permisos.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rol = models.ForeignKey(
        Roles,
        on_delete=models.CASCADE,
        related_name='permisos_asociados'
    )
    permiso = models.ForeignKey(
        Permisos,
        on_delete=models.CASCADE,
        related_name='roles_asociados'
    )
    
    # Metadata
    concedido_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles_permisos_extendidos'
        verbose_name = _('Rol-Permiso')
        verbose_name_plural = _('Roles-Permisos')
        unique_together = ('rol', 'permiso')

    def __str__(self):
        return f"{self.rol.nombre_rol} -> {self.permiso.nombre_permiso}"


class UsuariosRoles(models.Model):
    """
    Asignación de roles a usuarios.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.CASCADE,
        related_name='roles_asignados'
    )
    rol = models.ForeignKey(
        Roles,
        on_delete=models.CASCADE,
        related_name='usuarios_asignados'
    )
    
    # Alcance del rol
    empresa = models.ForeignKey(
        'usuarios.Empresas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Si el rol aplica solo a una empresa específica"
    )
    finca = models.ForeignKey(
        'usuarios.Fincas',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Si el rol aplica solo a una finca específica"
    )
    
    # Control
    es_activo = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    asignado_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roles_que_asigno'
    )
    motivo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'usuarios_roles_extendidos'
        verbose_name = _('Usuario-Rol')
        verbose_name_plural = _('Usuarios-Roles')
        unique_together = ('usuario', 'rol', 'empresa', 'finca')
        indexes = [
            models.Index(fields=['usuario', 'es_activo']),
            models.Index(fields=['rol']),
        ]

    def __str__(self):
        return f"{self.usuario.email} -> {self.rol.nombre_rol}"


class PermisosEspeciales(models.Model):
    """
    Permisos especiales asignados directamente a usuarios 
    sin pasar por roles.
    """
    TIPO_PERMISO_ESPECIAL = [
        ('CONCEDIDO', 'Permiso Concedido'),
        ('DENEGADO', 'Permiso Denegado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.CASCADE,
        related_name='permisos_especiales'
    )
    permiso = models.ForeignKey(
        Permisos,
        on_delete=models.CASCADE
    )
    tipo = models.CharField(max_length=20, choices=TIPO_PERMISO_ESPECIAL)
    
    # Alcance
    empresa = models.ForeignKey(
        'usuarios.Empresas',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # Control
    es_activo = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    concedido_por = models.ForeignKey(
        'autenticacion.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permisos_especiales_que_concedio'
    )
    motivo = models.TextField()

    class Meta:
        db_table = 'permisos_especiales'
        verbose_name = _('Permiso Especial')
        verbose_name_plural = _('Permisos Especiales')
        unique_together = ('usuario', 'permiso', 'empresa')
        indexes = [
            models.Index(fields=['usuario', 'es_activo']),
        ]

    def __str__(self):
        return f"{self.usuario.email} -> {self.permiso.nombre_permiso} ({self.tipo})"
