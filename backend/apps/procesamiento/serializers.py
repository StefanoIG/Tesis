from rest_framework import serializers
from apps.procesamiento.models import (
    ProcesosProcesamiento, InspeccionesCalidad,
    CertificacionesEstandares, ResultadosAnalisisLaboratorio
)


class ProcesosProcesimientoSerializer(serializers.ModelSerializer):
    """Serializer para ProcesosProcesamiento"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario_responsable.nombre_completo', read_only=True)

    class Meta:
        model = ProcesosProcesamiento
        fields = [
            'id', 'lote', 'lote_codigo', 'empresa', 'tipo_proceso',
            'descripcion', 'fecha_inicio', 'fecha_fin', 'usuario_responsable',
            'usuario_nombre', 'temperatura_promedio', 'humedad_promedio',
            'tiempo_duracion_minutos', 'resultado_proceso', 'observaciones',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


class InspeccionesCalidadSerializer(serializers.ModelSerializer):
    """Serializer para InspeccionesCalidad"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    inspector_nombre = serializers.CharField(source='inspector.nombre_completo', read_only=True)

    class Meta:
        model = InspeccionesCalidad
        fields = [
            'id', 'lote', 'lote_codigo', 'empresa', 'inspector', 'inspector_nombre',
            'tipo_inspeccion', 'fecha_inspeccion', 'resultado', 'porcentaje_rechazo',
            'criterios_evaluados', 'observaciones', 'recomendaciones',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


class CertificacionesEstandaresSerializer(serializers.ModelSerializer):
    """Serializer para CertificacionesEstandares"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)

    class Meta:
        model = CertificacionesEstandares
        fields = [
            'id', 'lote', 'lote_codigo', 'empresa', 'tipo_certificacion',
            'numero_certificado', 'fecha_emision', 'fecha_vencimiento',
            'organismo_certificador', 'auditor', 'documento_certificado',
            'es_valida', 'observaciones', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']


class ResultadosAnalisisLaboratorioSerializer(serializers.ModelSerializer):
    """Serializer para ResultadosAnalisisLaboratorio"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)

    class Meta:
        model = ResultadosAnalisisLaboratorio
        fields = [
            'id', 'lote', 'lote_codigo', 'empresa', 'tipo_analisis',
            'laboratorio', 'fecha_muestreo', 'fecha_resultado',
            'parametros_medidos', 'resultado_general', 'numero_informe',
            'documento_informe', 'observaciones', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']
