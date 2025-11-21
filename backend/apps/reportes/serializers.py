from rest_framework import serializers
from apps.reportes.models import Reportes, IndicesKPI, DashboardDatos
from datetime import datetime


class ReportesSerializer(serializers.ModelSerializer):
    """Serializer para Reportes"""
    usuario_nombre = serializers.CharField(source='usuario_creador.nombre_completo', read_only=True)
    formato = serializers.CharField(write_only=True, required=False)  # Alias para formato_exportacion
    incluir_graficos = serializers.BooleanField(write_only=True, required=False, default=True)

    class Meta:
        model = Reportes
        fields = [
            'id', 'nombre', 'descripcion', 'tipo_reporte', 'usuario_creador',
            'usuario_nombre', 'fecha_inicio', 'fecha_fin', 'filtros_aplicados',
            'datos_reporte', 'archivo_generado', 'formato_exportacion',
            'creado_en', 'actualizado_en', 'formato', 'incluir_graficos'
        ]
        read_only_fields = ['id', 'datos_reporte', 'archivo_generado', 'creado_en', 'actualizado_en']
        extra_kwargs = {
            'nombre': {'required': False},
            'fecha_inicio': {'required': False},
            'fecha_fin': {'required': False},
        }

    def validate(self, data):
        # Generar nombre automáticamente si no se proporciona
        if 'nombre' not in data or not data.get('nombre'):
            tipo = data.get('tipo_reporte', 'REPORTE')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            data['nombre'] = f"Reporte {tipo} - {timestamp}"
        
        # Si se pasa 'formato' en lugar de 'formato_exportacion'
        if 'formato' in data:
            data['formato_exportacion'] = data.pop('formato')
        
        # Asegurar que formato_exportacion tenga un valor válido
        if 'formato_exportacion' not in data:
            data['formato_exportacion'] = 'PDF'
        
        # Asegurar que fecha_inicio y fecha_fin tengan valores por defecto
        if 'fecha_inicio' not in data or not data.get('fecha_inicio'):
            from datetime import date, timedelta
            data['fecha_fin'] = date.today()
            data['fecha_inicio'] = data['fecha_fin'] - timedelta(days=30)
        elif 'fecha_fin' not in data or not data.get('fecha_fin'):
            from datetime import date
            data['fecha_fin'] = date.today()
        
        return data

    def create(self, validated_data):
        # Remover campos no relacionados con el modelo
        validated_data.pop('incluir_graficos', None)
        
        # Asignar usuario creador automáticamente
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['usuario_creador'] = request.user
        
        return super().create(validated_data)


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
