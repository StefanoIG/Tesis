from rest_framework import serializers
from apps.documentos.models import Documentos, FotosProductos


class DocumentosSerializer(serializers.ModelSerializer):
    """Serializer para Documentos"""
    subido_por_nombre = serializers.CharField(source='subido_por.nombre_completo', read_only=True)
    validado_por_nombre = serializers.CharField(source='validado_por.nombre_completo', read_only=True)
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True, allow_null=True)

    class Meta:
        model = Documentos
        fields = [
            'id', 'lote', 'lote_codigo', 'evento_trazabilidad', 'usuario',
            'tipo_documento', 'nombre', 'descripcion', 'archivo',
            'tipo_archivo', 'tamaño_bytes', 'estado', 'es_autentico',
            'hash_documento', 'fecha_documento', 'fecha_vencimiento',
            'numero_referencia', 'subido_por', 'subido_por_nombre',
            'validado_por', 'validado_por_nombre', 'fecha_validacion',
            'comentarios_validacion', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = [
            'id', 'hash_documento', 'tamaño_bytes', 'creado_en', 'actualizado_en'
        ]


class DocumentosListaSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados de documentos"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True, allow_null=True)
    subido_por_nombre = serializers.CharField(source='subido_por.nombre_completo', read_only=True)

    class Meta:
        model = Documentos
        fields = [
            'id', 'lote_codigo', 'tipo_documento', 'nombre', 'estado',
            'subido_por_nombre', 'creado_en'
        ]


class FotosProductosSerializer(serializers.ModelSerializer):
    """Serializer para FotosProductos"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True)
    fotografo_nombre = serializers.CharField(source='fotógrafo.nombre_completo', read_only=True)
    
    class Meta:
        model = FotosProductos
        fields = [
            'id', 'lote', 'lote_codigo', 'imagen', 'descripcion',
            'tipo_foto', 'latitud', 'longitud', 'fotógrafo',
            'fotografo_nombre', 'fecha_foto'
        ]
        read_only_fields = ['id', 'fecha_foto']
