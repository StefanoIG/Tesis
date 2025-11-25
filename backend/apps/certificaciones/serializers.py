from rest_framework import serializers
from .models import (
    Certificaciones, CertificacionesProductores, CertificacionesLotes,
    RequisitosCumplimiento, CumplimientoNormativo
)


class CertificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificaciones
        fields = [
            'id', 'nombre', 'codigo', 'tipo_certificacion',
            'entidad_emisora', 'alcance', 'descripcion',
            'requisitos', 'url_informacion', 'logo_url',
            'vigencia_anios', 'es_activa',
            'creado_en', 'actualizado_en'
        ]


class CertificacionesProductoresSerializer(serializers.ModelSerializer):
    certificacion_detalle = CertificacionesSerializer(source='certificacion', read_only=True)
    productor_nombre = serializers.CharField(source='productor.nombre', read_only=True)
    finca_nombre = serializers.CharField(source='finca.nombre', read_only=True)
    dias_para_expiracion = serializers.SerializerMethodField()
    estado_actual = serializers.SerializerMethodField()

    class Meta:
        model = CertificacionesProductores
        fields = [
            'id', 'certificacion', 'certificacion_detalle',
            'productor', 'productor_nombre',
            'finca', 'finca_nombre',
            'numero_certificado', 'fecha_emision', 'fecha_expiracion',
            'estado', 'estado_actual', 'dias_para_expiracion',
            'archivo_certificado', 'alcance_productos', 'alcance_procesos',
            'fecha_ultima_auditoria', 'fecha_proxima_auditoria',
            'auditor_nombre', 'observaciones', 'condiciones_especiales',
            'creado_en', 'actualizado_en'
        ]

    def get_dias_para_expiracion(self, obj):
        from django.utils import timezone
        dias = (obj.fecha_expiracion - timezone.now().date()).days
        return dias

    def get_estado_actual(self, obj):
        return obj.actualizar_estado()


class CertificacionesLotesSerializer(serializers.ModelSerializer):
    certificacion_nombre = serializers.CharField(
        source='certificacion_productor.certificacion.nombre',
        read_only=True
    )
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    verificado_por_nombre = serializers.CharField(
        source='verificado_por.nombre_completo',
        read_only=True
    )

    class Meta:
        model = CertificacionesLotes
        fields = [
            'id', 'lote', 'lote_codigo',
            'certificacion_productor', 'certificacion_nombre',
            'verificado', 'verificado_por', 'verificado_por_nombre',
            'fecha_verificacion', 'archivo_evidencia',
            'observaciones', 'creado_en'
        ]


class RequisitosCumplimientoSerializer(serializers.ModelSerializer):
    certificacion_nombre = serializers.CharField(
        source='certificacion.nombre',
        read_only=True
    )

    class Meta:
        model = RequisitosCumplimiento
        fields = [
            'id', 'certificacion', 'certificacion_nombre',
            'codigo_requisito', 'nombre', 'normativa', 'pais_destino',
            'descripcion', 'tipo_requisito', 'es_obligatorio',
            'frecuencia_verificacion', 'documentacion_requerida',
            'parametros_analisis', 'es_activo',
            'creado_en', 'actualizado_en'
        ]


class CumplimientoNormativoSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    requisito_detalle = RequisitosCumplimientoSerializer(source='requisito', read_only=True)
    verificado_por_nombre = serializers.CharField(
        source='verificado_por.nombre_completo',
        read_only=True
    )

    class Meta:
        model = CumplimientoNormativo
        fields = [
            'id', 'lote', 'lote_codigo',
            'requisito', 'requisito_detalle',
            'cumplido', 'fecha_verificacion',
            'verificado_por', 'verificado_por_nombre',
            'evidencia_url', 'archivo_evidencia',
            'numero_referencia', 'observaciones',
            'datos_verificacion',
            'creado_en', 'actualizado_en'
        ]
