from rest_framework import serializers
from apps.reportes.models import Reportes, IndicesKPI, DashboardDatos


class ReportesSerializer(serializers.ModelSerializer):
    """Serializer para Reportes"""
    usuario_nombre = serializers.CharField(source='usuario_creador.nombre_completo', read_only=True)

    class Meta:
        model = Reportes
        fields = [
            'id', 'nombre', 'descripcion', 'tipo_reporte', 'usuario_creador',
            'usuario_nombre', 'fecha_inicio', 'fecha_fin', 'filtros_aplicados',
            'datos_reporte', 'archivo_generado', 'formato_exportacion',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'datos_reporte', 'archivo_generado', 'creado_en', 'actualizado_en']


class IndicesKPISerializer(serializers.ModelSerializer):
    """Serializer para IndicesKPI"""
    class Meta:
        model = IndicesKPI
        fields = [
            'id', 'produccion_total_kg', 'numero_lotes_registrados',
            'numero_productos_diferentes', 'porcentaje_aprobados',
            'porcentaje_rechazados', 'porcentaje_condicionados',
            'entregas_a_tiempo', 'entregas_retrasadas',
            'tiempo_promedio_transporte_horas', 'certificaciones_activas',
            'porcentaje_cumplimiento_normativo', 'incidencias_reportadas',
            'fecha_inicio_periodo', 'fecha_fin_periodo', 'calculado_en'
        ]
        read_only_fields = ['id', 'calculado_en']


class DashboardDatosSerializer(serializers.ModelSerializer):
    """Serializer para DashboardDatos"""
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = DashboardDatos
        fields = [
            'id', 'usuario', 'usuario_email', 'tipo_dashboard', 'datos',
            'fecha_ultima_actualizacion', 'creado_en'
        ]
        read_only_fields = ['id', 'fecha_ultima_actualizacion', 'creado_en']
