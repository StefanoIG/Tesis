from rest_framework import serializers
from apps.alertas.models import ReglasAlertas, Alertas


class ReglasAlertasSerializer(serializers.ModelSerializer):
    """Serializer para ReglasAlertas"""
    class Meta:
        model = ReglasAlertas
        fields = [
            'id', 'nombre', 'descripcion', 'es_activa', 'tipo_alerta',
            'campo_monitoreado', 'operador', 'valor_comparacion',
            'severidad', 'notificar_roles', 'notificar_usuarios',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


class AlertasSerializer(serializers.ModelSerializer):
    """Serializer para Alertas"""
    lote_codigo = serializers.CharField(source='lote.codigo_lote', read_only=True, allow_null=True)
    usuario_asignado_nombre = serializers.CharField(
        source='usuario_asignado.nombre_completo',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Alertas
        fields = [
            'id', 'regla', 'lote', 'lote_codigo', 'envio', 'titulo',
            'descripcion', 'valor_actual', 'valor_umbral', 'estado',
            'severidad', 'usuario_asignado', 'usuario_asignado_nombre',
            'fecha_resolucion', 'comentario_resolucion', 'accion_tomada',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']
