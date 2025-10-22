from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# ========== ADMIN CUSTOMIZATION ==========
admin.site.site_header = 'Sistema de Trazabilidad Agroindustrial'
admin.site.site_title = 'Admin Trazabilidad'
admin.site.index_title = 'Bienvenido al Panel de Administración'

from apps.autenticacion.models import Usuarios, Roles, UsuariosRoles, Auditorias
from apps.usuarios.models import Empresas, Fincas, UsuariosEmpresas, Permisos, RolesPermisos
from apps.trazabilidad.models import Productos, Lotes, TiposEventosTrazabilidad, EventosTrazabilidad, HistorialEstadosLote
from apps.procesamiento.models import ProcesosProcesamiento, InspeccionesCalidad, CertificacionesEstandares, ResultadosAnalisisLaboratorio
from apps.logistica.models import Vehiculos, Conductores, Envios, RuteTrackingActual, AlertasLogistica
from apps.reportes.models import Reportes, IndicesKPI, DashboardDatos
from apps.documentos.models import Documentos, FotosProductos
from apps.sincronizacion.models import EstadosSincronizacion, ConflictosSincronizacion, RegistrosSincronizacion, ControlVersionesDB
from apps.administracion.models import ConfiguracionSistema, LogsAcceso, LogsActividad, BackupsSistema
from apps.alertas.models import ReglasAlertas, Alertas
from apps.notificaciones.models import Notificaciones, PreferenciasNotificaciones, HistorialLecturaNotifc

# ==================== AUTENTICACIÓN ====================
@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre_completo', 'activo', 'ultimo_acceso', 'creado_en')
    list_filter = ('activo', 'creado_en')
    search_fields = ('email', 'nombre_completo')
    readonly_fields = ('id', 'creado_en', 'actualizado_en')
    fieldsets = (
        (_('Información Personal'), {
            'fields': ('id', 'username', 'email', 'nombre_completo', 'telefono')
        }),
        (_('Seguridad'), {
            'fields': ('password',)
        }),
        (_('Permisos'), {
            'fields': ('is_staff', 'is_superuser', 'activo')
        }),
        (_('Fechas'), {
            'fields': ('ultimo_acceso', 'creado_en', 'actualizado_en')
        }),
    )

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('nombre_rol', 'descripcion')
    search_fields = ('nombre_rol',)

@admin.register(UsuariosRoles)
class UsuariosRolesAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'asignado_en')
    list_filter = ('rol', 'asignado_en')
    search_fields = ('usuario__email', 'rol__nombre_rol')

@admin.register(Auditorias)
class AuditoriasAdmin(admin.ModelAdmin):
    list_display = ('accion', 'usuario', 'entidad_afectada', 'resultado', 'timestamp')
    list_filter = ('resultado', 'entidad_afectada', 'timestamp')
    search_fields = ('usuario__email', 'accion')
    readonly_fields = ('id', 'timestamp')

# ==================== USUARIOS Y EMPRESAS ====================
@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_empresa', 'es_activa', 'creado_en')
    list_filter = ('tipo_empresa', 'es_activa')
    search_fields = ('nombre', 'registro_nacional')

@admin.register(Fincas)
class FincasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'codigo_finca', 'es_activa')
    list_filter = ('empresa', 'es_activa')
    search_fields = ('nombre', 'codigo_finca')

@admin.register(UsuariosEmpresas)
class UsuariosEmpresasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'empresa', 'es_responsable', 'fecha_asignacion')
    list_filter = ('es_responsable', 'empresa')
    search_fields = ('usuario__email', 'empresa__nombre')

@admin.register(Permisos)
class PermisosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo')
    search_fields = ('nombre', 'codigo')

# ==================== TRAZABILIDAD ====================
@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_producto', 'unidad_medida')
    list_filter = ('tipo_producto',)
    search_fields = ('nombre',)

@admin.register(Lotes)
class LotesAdmin(admin.ModelAdmin):
    list_display = ('codigo_lote', 'producto', 'cantidad', 'estado', 'fecha_produccion')
    list_filter = ('estado', 'es_organico', 'fecha_produccion')
    search_fields = ('codigo_lote', 'producto__nombre')
    readonly_fields = ('id', 'creado_en', 'actualizado_en')

@admin.register(TiposEventosTrazabilidad)
class TiposEventosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

@admin.register(EventosTrazabilidad)
class EventosTrazabilidadAdmin(admin.ModelAdmin):
    list_display = ('lote', 'tipo_evento', 'usuario', 'fecha_evento')
    list_filter = ('tipo_evento', 'fecha_evento')
    search_fields = ('lote__codigo_lote',)
    readonly_fields = ('id', 'timestamp_registro')

@admin.register(HistorialEstadosLote)
class HistorialEstadosLoteAdmin(admin.ModelAdmin):
    list_display = ('lote', 'estado_anterior', 'estado_nuevo', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('lote__codigo_lote',)
    readonly_fields = ('id', 'timestamp')

# ==================== PROCESAMIENTO ====================
@admin.register(ProcesosProcesamiento)
class ProcesosProcesimientoAdmin(admin.ModelAdmin):
    list_display = ('lote', 'tipo_proceso', 'empresa', 'fecha_inicio')
    list_filter = ('tipo_proceso', 'empresa')

@admin.register(InspeccionesCalidad)
class InspeccionesCalidadAdmin(admin.ModelAdmin):
    list_display = ('lote', 'tipo_inspeccion', 'resultado', 'fecha_inspeccion')
    list_filter = ('resultado', 'fecha_inspeccion')
    search_fields = ('lote__codigo_lote',)

@admin.register(CertificacionesEstandares)
class CertificacionesEstandaresAdmin(admin.ModelAdmin):
    list_display = ('numero_certificado', 'tipo_certificacion', 'es_valida', 'fecha_vencimiento')
    list_filter = ('tipo_certificacion', 'es_valida')

@admin.register(ResultadosAnalisisLaboratorio)
class ResultadosAnalisisLaboratorioAdmin(admin.ModelAdmin):
    list_display = ('numero_informe', 'tipo_analisis', 'laboratorio', 'resultado_general')
    list_filter = ('resultado_general', 'fecha_resultado')
    search_fields = ('numero_informe',)

# ==================== LOGÍSTICA ====================
@admin.register(Vehiculos)
class VehiculosAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'estado', 'es_refrigerado')
    list_filter = ('tipo_vehiculo', 'estado', 'es_refrigerado')
    search_fields = ('placa',)

@admin.register(Conductores)
class ConductoresAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'numero_licencia', 'es_activo')
    list_filter = ('es_activo', 'categoria_licencia')
    search_fields = ('numero_licencia', 'usuario__email')

@admin.register(Envios)
class EnviosAdmin(admin.ModelAdmin):
    list_display = ('lote', 'nombre_origen', 'nombre_destino', 'estado', 'fecha_salida')
    list_filter = ('estado', 'fecha_salida')
    search_fields = ('lote__codigo_lote',)

@admin.register(RuteTrackingActual)
class RuteTrackingActualAdmin(admin.ModelAdmin):
    list_display = ('envio', 'latitud', 'longitud', 'temperatura', 'timestamp')
    list_filter = ('timestamp',)

@admin.register(AlertasLogistica)
class AlertasLogisticaAdmin(admin.ModelAdmin):
    list_display = ('envio', 'tipo_alerta', 'estado_alerta', 'fecha_alerta')
    list_filter = ('tipo_alerta', 'estado_alerta')

# ==================== REPORTES ====================
@admin.register(Reportes)
class ReportesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_reporte', 'usuario_creador', 'creado_en')
    list_filter = ('tipo_reporte', 'creado_en')
    search_fields = ('nombre',)

@admin.register(IndicesKPI)
class IndicesKPIAdmin(admin.ModelAdmin):
    list_display = ('produccion_total_kg', 'numero_lotes_registrados', 'fecha_inicio_periodo')
    list_filter = ('fecha_inicio_periodo',)
    readonly_fields = ('calculado_en',)

@admin.register(DashboardDatos)
class DashboardDatosAdmin(admin.ModelAdmin):
    list_display = ('tipo_dashboard', 'usuario', 'fecha_ultima_actualizacion')
    list_filter = ('tipo_dashboard',)

# ==================== DOCUMENTOS ====================
@admin.register(Documentos)
class DocumentosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_documento', 'estado', 'subido_por', 'creado_en')
    list_filter = ('tipo_documento', 'estado', 'creado_en')
    search_fields = ('nombre',)

@admin.register(FotosProductos)
class FotosProductosAdmin(admin.ModelAdmin):
    list_display = ('lote', 'tipo_foto', 'fotógrafo', 'fecha_foto')
    list_filter = ('tipo_foto', 'fecha_foto')

# ==================== SINCRONIZACIÓN ====================
@admin.register(EstadosSincronizacion)
class EstadosSincronizacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo_dispositivo', 'estado', 'ultimo_sync_exitoso')
    list_filter = ('plataforma', 'estado')

@admin.register(ConflictosSincronizacion)
class ConflictosSincronizacionAdmin(admin.ModelAdmin):
    list_display = ('tabla_afectada', 'estado_conflicto', 'detectado_en')
    list_filter = ('estado_conflicto', 'detectado_en')

@admin.register(RegistrosSincronizacion)
class RegistrosSincronizacionAdmin(admin.ModelAdmin):
    list_display = ('sincronizacion', 'tipo_sincronizacion', 'fue_exitosa', 'timestamp_inicio')
    list_filter = ('fue_exitosa', 'tipo_sincronizacion')

@admin.register(ControlVersionesDB)
class ControlVersionesDBAdmin(admin.ModelAdmin):
    list_display = ('numero_version', 'fecha_liberacion', 'es_obligatoria')
    list_filter = ('es_obligatoria', 'fecha_liberacion')

# ==================== ADMINISTRACIÓN ====================
@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ('actualizado_en',)

@admin.register(LogsAcceso)
class LogsAccesoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_acceso', 'ip_origen', 'timestamp')
    list_filter = ('tipo_acceso', 'timestamp')
    search_fields = ('usuario__email', 'ip_origen')
    readonly_fields = ('id', 'timestamp')

@admin.register(LogsActividad)
class LogsActividadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_actividad', 'modulo', 'entidad', 'timestamp')
    list_filter = ('tipo_actividad', 'modulo', 'timestamp')
    readonly_fields = ('id', 'timestamp')

@admin.register(BackupsSistema)
class BackupsSistemaAdmin(admin.ModelAdmin):
    list_display = ('tipo_backup', 'estado', 'fecha_inicio', 'tamaño_mb')
    list_filter = ('estado', 'tipo_backup', 'fecha_inicio')

# ==================== ALERTAS ====================
@admin.register(ReglasAlertas)
class ReglasAlertasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_alerta', 'es_activa', 'severidad')
    list_filter = ('es_activa', 'severidad')

@admin.register(Alertas)
class AlertasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'severidad', 'usuario_asignado', 'creado_en')
    list_filter = ('estado', 'severidad', 'creado_en')
    search_fields = ('titulo',)

# ==================== NOTIFICACIONES ====================
@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario_destinatario', 'tipo_notificacion', 'fue_leida', 'creado_en')
    list_filter = ('tipo_notificacion', 'fue_leida', 'prioridad')
    search_fields = ('titulo', 'usuario_destinatario__email')

@admin.register(PreferenciasNotificaciones)
class PreferenciasNotificacionesAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'intervalo_polling_segundos')

@admin.register(HistorialLecturaNotifc)
class HistorialLecturaNotificacionesAdmin(admin.ModelAdmin):
    list_display = ('notificacion', 'tipo_dispositivo', 'timestamp_lectura')
    list_filter = ('tipo_dispositivo', 'timestamp_lectura')
