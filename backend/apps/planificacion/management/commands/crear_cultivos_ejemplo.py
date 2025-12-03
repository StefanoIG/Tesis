"""
Comando para crear cultivos de ejemplo en el catálogo
Ejecutar: python manage.py crear_cultivos_ejemplo
"""
from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.planificacion.models import CatalogosCultivos


class Command(BaseCommand):
    help = 'Crea cultivos de ejemplo en el catálogo'

    def handle(self, *args, **options):
        cultivos_data = [
            {
                'nombre_comun': 'Rosas',
                'nombre_cientifico': 'Rosa spp.',
                'categoria': 'FLORES',
                'variedades': ['Freedom', 'Vendela', 'Explorer'],
                'ph_minimo': Decimal('5.5'),
                'ph_maximo': Decimal('7.0'),
                'ph_optimo_min': Decimal('6.0'),
                'ph_optimo_max': Decimal('6.5'),
                'temperatura_min': Decimal('15.0'),
                'temperatura_max': Decimal('25.0'),
                'temperatura_optima_min': Decimal('16.0'),
                'temperatura_optima_max': Decimal('20.0'),
                'precipitacion_anual_min': 800,
                'precipitacion_anual_max': 1200,
                'altitud_minima': 2400,
                'altitud_maxima': 3000,
                'texturas_compatibles': ['FRANCO', 'FRANCO_ARENOSO', 'FRANCO_ARCILLOSO'],
                'nivel_dificultad': 'DIFICIL',
                'dias_hasta_cosecha': 90,
                'dias_germinacion': 14,
                'ciclos_por_anio': 4,
                'frecuencia_riego_dias': 2,
                'requiere_riego_constante': True,
                'rendimiento_promedio_hectarea': Decimal('250000'),  # tallos
                'precio_mercado_promedio': Decimal('0.50'),  # USD por tallo
                'demanda_mercado': 'MUY_ALTA',
                'certificaciones_recomendadas': ['FLORVERDE', 'RAINFOREST_ALLIANCE'],
                'es_activo': True,
            },
            {
                'nombre_comun': 'Cacao',
                'nombre_cientifico': 'Theobroma cacao',
                'categoria': 'OTROS',
                'variedades': ['CCN-51', 'Nacional'],
                'ph_minimo': Decimal('6.0'),
                'ph_maximo': Decimal('7.5'),
                'ph_optimo_min': Decimal('6.5'),
                'ph_optimo_max': Decimal('7.0'),
                'temperatura_min': Decimal('21.0'),
                'temperatura_max': Decimal('32.0'),
                'temperatura_optima_min': Decimal('23.0'),
                'temperatura_optima_max': Decimal('28.0'),
                'precipitacion_anual_min': 1500,
                'precipitacion_anual_max': 2500,
                'altitud_minima': 0,
                'altitud_maxima': 800,
                'texturas_compatibles': ['FRANCO', 'FRANCO_ARCILLOSO'],
                'nivel_dificultad': 'MODERADO',
                'dias_hasta_cosecha': 1095,  # 3 años
                'dias_germinacion': 30,
                'ciclos_por_anio': 1,
                'frecuencia_riego_dias': 7,
                'requiere_riego_constante': False,
                'rendimiento_promedio_hectarea': Decimal('800'),  # kg
                'precio_mercado_promedio': Decimal('3.50'),  # USD por kg
                'demanda_mercado': 'ALTA',
                'certificaciones_recomendadas': ['ORGANICO', 'UTZ', 'FAIRTRADE'],
                'es_activo': True,
            },
            {
                'nombre_comun': 'Banano',
                'nombre_cientifico': 'Musa paradisiaca',
                'categoria': 'FRUTAS',
                'variedades': ['Cavendish', 'Williams'],
                'ph_minimo': Decimal('5.5'),
                'ph_maximo': Decimal('7.5'),
                'ph_optimo_min': Decimal('6.0'),
                'ph_optimo_max': Decimal('7.0'),
                'temperatura_min': Decimal('15.0'),
                'temperatura_max': Decimal('35.0'),
                'temperatura_optima_min': Decimal('25.0'),
                'temperatura_optima_max': Decimal('30.0'),
                'precipitacion_anual_min': 2000,
                'precipitacion_anual_max': 4000,
                'altitud_minima': 0,
                'altitud_maxima': 300,
                'texturas_compatibles': ['FRANCO', 'FRANCO_ARCILLOSO'],
                'nivel_dificultad': 'FACIL',
                'dias_hasta_cosecha': 270,
                'dias_germinacion': 0,
                'ciclos_por_anio': 1,
                'frecuencia_riego_dias': 5,
                'requiere_riego_constante': True,
                'rendimiento_promedio_hectarea': Decimal('2500'),  # cajas
                'precio_mercado_promedio': Decimal('6.50'),  # USD por caja
                'demanda_mercado': 'MUY_ALTA',
                'certificaciones_recomendadas': ['GLOBALGAP', 'RAINFOREST_ALLIANCE'],
                'es_activo': True,
            },
            {
                'nombre_comun': 'Café Arábica',
                'nombre_cientifico': 'Coffea arabica',
                'categoria': 'OTROS',
                'variedades': ['Típica', 'Caturra', 'Bourbon'],
                'ph_minimo': Decimal('5.0'),
                'ph_maximo': Decimal('6.5'),
                'ph_optimo_min': Decimal('5.5'),
                'ph_optimo_max': Decimal('6.0'),
                'temperatura_min': Decimal('15.0'),
                'temperatura_max': Decimal('24.0'),
                'temperatura_optima_min': Decimal('17.0'),
                'temperatura_optima_max': Decimal('21.0'),
                'precipitacion_anual_min': 1500,
                'precipitacion_anual_max': 2500,
                'altitud_minima': 1200,
                'altitud_maxima': 2000,
                'texturas_compatibles': ['FRANCO', 'FRANCO_ARENOSO'],
                'nivel_dificultad': 'MODERADO',
                'dias_hasta_cosecha': 1095,  # 3 años
                'dias_germinacion': 45,
                'ciclos_por_anio': 1,
                'frecuencia_riego_dias': 10,
                'requiere_riego_constante': False,
                'rendimiento_promedio_hectarea': Decimal('1200'),  # kg
                'precio_mercado_promedio': Decimal('4.00'),  # USD por kg
                'demanda_mercado': 'ALTA',
                'certificaciones_recomendadas': ['ORGANICO', 'FAIRTRADE', 'RAINFOREST_ALLIANCE'],
                'es_activo': True,
            },
            {
                'nombre_comun': 'Aguacate Hass',
                'nombre_cientifico': 'Persea americana',
                'categoria': 'FRUTAS',
                'variedades': ['Hass'],
                'ph_minimo': Decimal('5.0'),
                'ph_maximo': Decimal('7.0'),
                'ph_optimo_min': Decimal('6.0'),
                'ph_optimo_max': Decimal('6.5'),
                'temperatura_min': Decimal('13.0'),
                'temperatura_max': Decimal('25.0'),
                'temperatura_optima_min': Decimal('18.0'),
                'temperatura_optima_max': Decimal('22.0'),
                'precipitacion_anual_min': 1000,
                'precipitacion_anual_max': 1500,
                'altitud_minima': 800,
                'altitud_maxima': 2500,
                'texturas_compatibles': ['FRANCO', 'FRANCO_ARENOSO'],
                'nivel_dificultad': 'FACIL',
                'dias_hasta_cosecha': 1460,  # 4 años
                'dias_germinacion': 30,
                'ciclos_por_anio': 1,
                'frecuencia_riego_dias': 7,
                'requiere_riego_constante': False,
                'rendimiento_promedio_hectarea': Decimal('10000'),  # kg
                'precio_mercado_promedio': Decimal('2.50'),  # USD por kg
                'demanda_mercado': 'MUY_ALTA',
                'certificaciones_recomendadas': ['GLOBALGAP', 'ORGANICO'],
                'es_activo': True,
            },
            {
                'nombre_comun': 'Brócoli',
                'nombre_cientifico': 'Brassica oleracea var. italica',
                'categoria': 'HORTALIZAS',
                'variedades': ['Legacy', 'Marathon'],
                'ph_minimo': Decimal('6.0'),
                'ph_maximo': Decimal('7.0'),
                'ph_optimo_min': Decimal('6.5'),
                'ph_optimo_max': Decimal('7.0'),
                'temperatura_min': Decimal('15.0'),
                'temperatura_max': Decimal('20.0'),
                'temperatura_optima_min': Decimal('16.0'),
                'temperatura_optima_max': Decimal('18.0'),
                'precipitacion_anual_min': 600,
                'precipitacion_anual_max': 900,
                'altitud_minima': 2400,
                'altitud_maxima': 3200,
                'texturas_compatibles': ['FRANCO', 'FRANCO_ARCILLOSO'],
                'nivel_dificultad': 'FACIL',
                'dias_hasta_cosecha': 90,
                'dias_germinacion': 7,
                'ciclos_por_anio': 3,
                'frecuencia_riego_dias': 3,
                'requiere_riego_constante': True,
                'rendimiento_promedio_hectarea': Decimal('15000'),  # kg
                'precio_mercado_promedio': Decimal('1.20'),  # USD por kg
                'demanda_mercado': 'ALTA',
                'certificaciones_recomendadas': ['GLOBALGAP'],
                'es_activo': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for cultivo_data in cultivos_data:
            cultivo, created = CatalogosCultivos.objects.update_or_create(
                nombre_comun=cultivo_data['nombre_comun'],
                defaults=cultivo_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {cultivo.nombre_comun}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'  Actualizado: {cultivo.nombre_comun}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado: {created_count} creados, {updated_count} actualizados'
            )
        )
