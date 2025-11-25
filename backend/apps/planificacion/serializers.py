from rest_framework import serializers
from .models import (
    EstudiosSuelo, Parcelas, CatalogosCultivos, PlanesCultivo,
    CalendariosRiego, RegistrosRiego, PermisosNacionalesEcuador, PermisosObtenidos
)


class EstudiosSueloSerializer(serializers.ModelSerializer):
    finca_nombre = serializers.CharField(source='finca.nombre', read_only=True)
    parcela_nombre = serializers.CharField(source='parcela.nombre', read_only=True)
    
    class Meta:
        model = EstudiosSuelo
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')


class ParcelasSerializer(serializers.ModelSerializer):
    finca_nombre = serializers.CharField(source='finca.nombre', read_only=True)
    cultivo_actual_nombre = serializers.CharField(source='cultivo_actual.nombre_comun', read_only=True)
    area_m2 = serializers.SerializerMethodField()
    
    class Meta:
        model = Parcelas
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')
    
    def get_area_m2(self, obj):
        return float(obj.area_hectareas * 10000) if obj.area_hectareas else 0


class CatalogosCultivosSerializer(serializers.ModelSerializer):
    rentabilidad_estimada = serializers.SerializerMethodField()
    
    class Meta:
        model = CatalogosCultivos
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')
    
    def get_rentabilidad_estimada(self, obj):
        if obj.rendimiento_promedio_hectarea and obj.precio_mercado_promedio:
            return float(obj.rendimiento_promedio_hectarea * obj.precio_mercado_promedio)
        return None


class PlanesCultivoSerializer(serializers.ModelSerializer):
    parcela_nombre = serializers.CharField(source='parcela.nombre', read_only=True)
    cultivo_nombre = serializers.CharField(source='cultivo.nombre_comun', read_only=True)
    creado_por_nombre = serializers.CharField(source='creado_por.nombre_completo', read_only=True)
    dias_hasta_cosecha = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanesCultivo
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')
    
    def get_dias_hasta_cosecha(self, obj):
        if obj.fecha_planificada_siembra and obj.fecha_estimada_cosecha:
            return (obj.fecha_estimada_cosecha - obj.fecha_planificada_siembra).days
        return None


class CalendariosRiegoSerializer(serializers.ModelSerializer):
    plan_cultivo_info = serializers.SerializerMethodField()
    sensor_nombre = serializers.CharField(source='sensor_humedad.nombre', read_only=True)
    
    class Meta:
        model = CalendariosRiego
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')
    
    def get_plan_cultivo_info(self, obj):
        return {
            'parcela': obj.plan_cultivo.parcela.nombre,
            'cultivo': obj.plan_cultivo.cultivo.nombre_comun
        }


class RegistrosRiegoSerializer(serializers.ModelSerializer):
    ejecutado_por_nombre = serializers.CharField(source='ejecutado_por.nombre_completo', read_only=True)
    parcela_nombre = serializers.CharField(source='calendario.plan_cultivo.parcela.nombre', read_only=True)
    
    class Meta:
        model = RegistrosRiego
        fields = '__all__'
        read_only_fields = ('creado_en',)


class PermisosNacionalesEcuadorSerializer(serializers.ModelSerializer):
    cultivos_aplicables_nombres = serializers.SerializerMethodField()
    
    class Meta:
        model = PermisosNacionalesEcuador
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')
    
    def get_cultivos_aplicables_nombres(self, obj):
        return list(obj.cultivos_aplicables.values_list('nombre_comun', flat=True))


class PermisosObtenidosSerializer(serializers.ModelSerializer):
    permiso_nombre = serializers.CharField(source='permiso.nombre_permiso', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    finca_nombre = serializers.CharField(source='finca.nombre', read_only=True)
    dias_hasta_vencimiento = serializers.SerializerMethodField()
    
    class Meta:
        model = PermisosObtenidos
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')
    
    def get_dias_hasta_vencimiento(self, obj):
        from django.utils import timezone
        if obj.fecha_vencimiento:
            delta = obj.fecha_vencimiento - timezone.now().date()
            return delta.days
        return None
