"""
Script para crear cultivos de ejemplo
Ejecutar: python manage.py shell < crear_cultivos.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from decimal import Decimal
from apps.planificacion.models import CatalogosCultivos

cultivos_data = [
    {
        'nombre_comun': 'Rosas',
        'nombre_cientifico': 'Rosa spp.',
        'familia': 'Rosaceae',
        'tipo_cultivo': 'FLOR',
        'descripcion': 'Flores de corte premium para exportación',
        'ph_minimo': Decimal('5.5'),
        'ph_maximo': Decimal('7.0'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('6.5'),
        'temperatura_min': Decimal('15.0'),
        'temperatura_max': Decimal('25.0'),
        'temperatura_optima': Decimal('18.0'),
        'precipitacion_anual_min': Decimal('800'),
        'precipitacion_anual_max': Decimal('1200'),
        'altitud_min': Decimal('2400'),
        'altitud_max': Decimal('3000'),
        'texturas_compatibles': ['Franco', 'Franco-arenoso', 'Franco-arcilloso'],
        'requerimiento_nitrogeno': 'ALTO',
        'requerimiento_fosforo': 'MEDIO',
        'requerimiento_potasio': 'ALTO',
        'nivel_dificultad': 'ALTO',
        'dias_hasta_cosecha': 90,
        'rendimiento_promedio_hectarea': Decimal('250000'),
        'precio_mercado_promedio': Decimal('0.50'),
        'demanda_mercado': 'MUY_ALTA',
        'es_activo': True,
    },
    {
        'nombre_comun': 'Cacao',
        'nombre_cientifico': 'Theobroma cacao',
        'familia': 'Malvaceae',
        'tipo_cultivo': 'PERENNE',
        'descripcion': 'Cacao fino de aroma ecuatoriano',
        'ph_minimo': Decimal('6.0'),
        'ph_maximo': Decimal('7.5'),
        'ph_optimo_min': Decimal('6.5'),
        'ph_optimo_max': Decimal('7.0'),
        'temperatura_min': Decimal('21.0'),
        'temperatura_max': Decimal('32.0'),
        'temperatura_optima': Decimal('25.0'),
        'precipitacion_anual_min': Decimal('1500'),
        'precipitacion_anual_max': Decimal('2500'),
        'altitud_min': Decimal('0'),
        'altitud_max': Decimal('800'),
        'texturas_compatibles': ['Franco', 'Franco-arcilloso'],
        'requerimiento_nitrogeno': 'MEDIO',
        'requerimiento_fosforo': 'MEDIO',
        'requerimiento_potasio': 'ALTO',
        'nivel_dificultad': 'MODERADO',
        'dias_hasta_cosecha': 1095,
        'rendimiento_promedio_hectarea': Decimal('800'),
        'precio_mercado_promedio': Decimal('3.50'),
        'demanda_mercado': 'ALTA',
        'es_activo': True,
    },
    {
        'nombre_comun': 'Banano',
        'nombre_cientifico': 'Musa paradisiaca',
        'familia': 'Musaceae',
        'tipo_cultivo': 'PERENNE',
        'descripcion': 'Banano Cavendish para exportación',
        'ph_minimo': Decimal('5.5'),
        'ph_maximo': Decimal('7.5'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('7.0'),
        'temperatura_min': Decimal('15.0'),
        'temperatura_max': Decimal('35.0'),
        'temperatura_optima': Decimal('27.0'),
        'precipitacion_anual_min': Decimal('2000'),
        'precipitacion_anual_max': Decimal('4000'),
        'altitud_min': Decimal('0'),
        'altitud_max': Decimal('300'),
        'texturas_compatibles': ['Franco', 'Franco-arcilloso'],
        'requerimiento_nitrogeno': 'ALTO',
        'requerimiento_fosforo': 'MEDIO',
        'requerimiento_potasio': 'ALTO',
        'nivel_dificultad': 'FACIL',
        'dias_hasta_cosecha': 270,
        'rendimiento_promedio_hectarea': Decimal('2500'),
        'precio_mercado_promedio': Decimal('6.50'),
        'demanda_mercado': 'MUY_ALTA',
        'es_activo': True,
    },
    {
        'nombre_comun': 'Café Arábica',
        'nombre_cientifico': 'Coffea arabica',
        'familia': 'Rubiaceae',
        'tipo_cultivo': 'PERENNE',
        'descripcion': 'Café de altura premium',
        'ph_minimo': Decimal('5.0'),
        'ph_maximo': Decimal('6.5'),
        'ph_optimo_min': Decimal('5.5'),
        'ph_optimo_max': Decimal('6.0'),
        'temperatura_min': Decimal('15.0'),
        'temperatura_max': Decimal('24.0'),
        'temperatura_optima': Decimal('18.0'),
        'precipitacion_anual_min': Decimal('1500'),
        'precipitacion_anual_max': Decimal('2500'),
        'altitud_min': Decimal('1200'),
        'altitud_max': Decimal('2000'),
        'texturas_compatibles': ['Franco', 'Franco-arenoso'],
        'requerimiento_nitrogeno': 'MEDIO',
        'requerimiento_fosforo': 'MEDIO',
        'requerimiento_potasio': 'MEDIO',
        'nivel_dificultad': 'MODERADO',
        'dias_hasta_cosecha': 1095,
        'rendimiento_promedio_hectarea': Decimal('1200'),
        'precio_mercado_promedio': Decimal('4.00'),
        'demanda_mercado': 'ALTA',
        'es_activo': True,
    },
    {
        'nombre_comun': 'Aguacate Hass',
        'nombre_cientifico': 'Persea americana',
        'familia': 'Lauraceae',
        'tipo_cultivo': 'PERENNE',
        'descripcion': 'Aguacate Hass para exportación',
        'ph_minimo': Decimal('5.0'),
        'ph_maximo': Decimal('7.0'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('6.5'),
        'temperatura_min': Decimal('13.0'),
        'temperatura_max': Decimal('25.0'),
        'temperatura_optima': Decimal('20.0'),
        'precipitacion_anual_min': Decimal('1000'),
        'precipitacion_anual_max': Decimal('1500'),
        'altitud_min': Decimal('800'),
        'altitud_max': Decimal('2500'),
        'texturas_compatibles': ['Franco', 'Franco-arenoso'],
        'requerimiento_nitrogeno': 'MEDIO',
        'requerimiento_fosforo': 'BAJO',
        'requerimiento_potasio': 'ALTO',
        'nivel_dificultad': 'FACIL',
        'dias_hasta_cosecha': 1460,
        'rendimiento_promedio_hectarea': Decimal('10000'),
        'precio_mercado_promedio': Decimal('2.50'),
        'demanda_mercado': 'MUY_ALTA',
        'es_activo': True,
    },
    {
        'nombre_comun': 'Brócoli',
        'nombre_cientifico': 'Brassica oleracea var. italica',
        'familia': 'Brassicaceae',
        'tipo_cultivo': 'HORTALIZA',
        'descripcion': 'Brócoli para mercado nacional y exportación',
        'ph_minimo': Decimal('6.0'),
        'ph_maximo': Decimal('7.0'),
        'ph_optimo_min': Decimal('6.5'),
        'ph_optimo_max': Decimal('7.0'),
        'temperatura_min': Decimal('15.0'),
        'temperatura_max': Decimal('20.0'),
        'temperatura_optima': Decimal('18.0'),
        'precipitacion_anual_min': Decimal('600'),
        'precipitacion_anual_max': Decimal('900'),
        'altitud_min': Decimal('2400'),
        'altitud_max': Decimal('3200'),
        'texturas_compatibles': ['Franco', 'Franco-arcilloso'],
        'requerimiento_nitrogeno': 'ALTO',
        'requerimiento_fosforo': 'MEDIO',
        'requerimiento_potasio': 'MEDIO',
        'nivel_dificultad': 'FACIL',
        'dias_hasta_cosecha': 90,
        'rendimiento_promedio_hectarea': Decimal('15000'),
        'precio_mercado_promedio': Decimal('1.20'),
        'demanda_mercado': 'ALTA',
        'es_activo': True,
    },
]

print("="*60)
print("CREANDO CULTIVOS DE EJEMPLO")
print("="*60)

created_count = 0
updated_count = 0

for cultivo_data in cultivos_data:
    cultivo, created = CatalogosCultivos.objects.update_or_create(
        nombre_comun=cultivo_data['nombre_comun'],
        defaults=cultivo_data
    )
    
    if created:
        created_count += 1
        print(f'✓ Creado: {cultivo.nombre_comun}')
    else:
        updated_count += 1
        print(f'  Actualizado: {cultivo.nombre_comun}')

print("="*60)
print(f'✅ Completado: {created_count} creados, {updated_count} actualizados')
print("="*60)
