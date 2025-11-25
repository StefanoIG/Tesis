"""
Script para poblar datos iniciales de planificación agrícola:
- Cultivos comunes de Ecuador
- Permisos nacionales (AGROCALIDAD, MAG, MAATE, etc.)
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from apps.planificacion.models import CatalogosCultivos, PermisosNacionalesEcuador


print("="*80)
print("POBLANDO DATOS DE PLANIFICACIÓN AGRÍCOLA")
print("="*80)

# ============================================================================
# CATÁLOGO DE CULTIVOS ECUATORIANOS
# ============================================================================
print("\n[1/2] Creando catálogo de cultivos ecuatorianos...")

cultivos_data = [
    # FLORES
    {
        'nombre_cientifico': 'Rosa spp.',
        'nombre_comun': 'Rosa',
        'categoria': 'FLORES',
        'variedades': ['Freedom', 'Vendela', 'Forever Young', 'Mondial', 'Engagement'],
        'ph_minimo': Decimal('5.5'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('6.5'),
        'ph_maximo': Decimal('7.0'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_ARENOSO', 'FRANCO_LIMOSO'],
        'temperatura_min': Decimal('10.0'),
        'temperatura_optima_min': Decimal('15.0'),
        'temperatura_optima_max': Decimal('25.0'),
        'temperatura_max': Decimal('30.0'),
        'altitud_minima': 2200,
        'altitud_maxima': 3000,
        'precipitacion_anual_min': 800,
        'precipitacion_anual_max': 1200,
        'dias_germinacion': 0,
        'dias_hasta_cosecha': 90,
        'ciclos_por_anio': 4,
        'frecuencia_riego_dias': 2,
        'litros_agua_por_planta_dia': Decimal('2.5'),
        'requiere_riego_constante': True,
        'rendimiento_promedio_hectarea': Decimal('180000'),  # tallos/año
        'precio_mercado_promedio': Decimal('0.30'),  # USD por tallo
        'demanda_mercado': 'MUY_ALTA',
        'nivel_dificultad': 'EXPERTO',
        'certificaciones_recomendadas': ['GlobalG.A.P.', 'Rainforest Alliance', 'Fair Trade', 'Florverde'],
        'permisos_requeridos_ecuador': ['Registro AGROCALIDAD', 'Certificado Fitosanitario'],
        'descripcion': 'Cultivo de rosas de exportación, principal producto florícola de Ecuador',
        'plagas_comunes': ['Trips', 'Ácaros', 'Pulgones', 'Botrytis'],
        'enfermedades_comunes': ['Mildiu velloso', 'Oidio', 'Roya'],
        'compatibilidad_rotacion': []
    },
    {
        'nombre_cientifico': 'Gypsophila paniculata',
        'nombre_comun': 'Gypsophila',
        'categoria': 'FLORES',
        'variedades': ['Million Stars', 'Overtime', 'My Pink'],
        'ph_minimo': Decimal('6.0'),
        'ph_optimo_min': Decimal('6.5'),
        'ph_optimo_max': Decimal('7.5'),
        'ph_maximo': Decimal('8.0'),
        'texturas_compatibles': ['FRANCO', 'ARENOSO', 'FRANCO_ARENOSO'],
        'temperatura_min': Decimal('10.0'),
        'temperatura_optima_min': Decimal('15.0'),
        'temperatura_optima_max': Decimal('22.0'),
        'temperatura_max': Decimal('28.0'),
        'altitud_minima': 2400,
        'altitud_maxima': 3200,
        'precipitacion_anual_min': 600,
        'precipitacion_anual_max': 1000,
        'dias_germinacion': 10,
        'dias_hasta_cosecha': 120,
        'ciclos_por_anio': 3,
        'frecuencia_riego_dias': 3,
        'litros_agua_por_planta_dia': Decimal('1.5'),
        'requiere_riego_constante': False,
        'rendimiento_promedio_hectarea': Decimal('120000'),
        'precio_mercado_promedio': Decimal('0.25'),
        'demanda_mercado': 'ALTA',
        'nivel_dificultad': 'MODERADO',
        'certificaciones_recomendadas': ['GlobalG.A.P.', 'Florverde'],
        'permisos_requeridos_ecuador': ['Registro AGROCALIDAD'],
        'descripcion': 'Flor complementaria muy demandada en arreglos florales',
        'plagas_comunes': ['Pulgones', 'Minadores'],
        'enfermedades_comunes': ['Fusarium', 'Pythium'],
        'compatibilidad_rotacion': []
    },
    
    # FRUTAS
    {
        'nombre_cientifico': 'Musa paradisiaca',
        'nombre_comun': 'Banano',
        'categoria': 'FRUTAS',
        'variedades': ['Cavendish', 'Gros Michel', 'Orito'],
        'ph_minimo': Decimal('5.5'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('7.0'),
        'ph_maximo': Decimal('7.5'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_ARCILLOSO', 'FRANCO_LIMOSO'],
        'temperatura_min': Decimal('15.0'),
        'temperatura_optima_min': Decimal('24.0'),
        'temperatura_optima_max': Decimal('30.0'),
        'temperatura_max': Decimal('35.0'),
        'altitud_minima': 0,
        'altitud_maxima': 300,
        'precipitacion_anual_min': 2000,
        'precipitacion_anual_max': 3000,
        'dias_germinacion': 0,
        'dias_hasta_cosecha': 270,
        'ciclos_por_anio': 1,
        'frecuencia_riego_dias': 3,
        'litros_agua_por_planta_dia': Decimal('25.0'),
        'requiere_riego_constante': True,
        'rendimiento_promedio_hectarea': Decimal('45'),  # toneladas
        'precio_mercado_promedio': Decimal('7.50'),  # USD por caja 18kg
        'demanda_mercado': 'MUY_ALTA',
        'nivel_dificultad': 'MODERADO',
        'certificaciones_recomendadas': ['GlobalG.A.P.', 'Rainforest Alliance', 'Orgánico'],
        'permisos_requeridos_ecuador': ['Código de Productor', 'Certificado Fitosanitario'],
        'descripcion': 'Principal producto de exportación agrícola de Ecuador',
        'plagas_comunes': ['Sigatoka negra', 'Picudo negro', 'Cochinilla'],
        'enfermedades_comunes': ['Mal de Panamá', 'Moko', 'Pudrición del cogollo'],
        'compatibilidad_rotacion': []
    },
    {
        'nombre_cientifico': 'Persea americana',
        'nombre_comun': 'Aguacate Hass',
        'categoria': 'FRUTAS',
        'variedades': ['Hass', 'Fuerte', 'Lorena'],
        'ph_minimo': Decimal('5.5'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('7.0'),
        'ph_maximo': Decimal('7.5'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_ARENOSO'],
        'temperatura_min': Decimal('13.0'),
        'temperatura_optima_min': Decimal('20.0'),
        'temperatura_optima_max': Decimal('25.0'),
        'temperatura_max': Decimal('30.0'),
        'altitud_minima': 1500,
        'altitud_maxima': 2400,
        'precipitacion_anual_min': 1000,
        'precipitacion_anual_max': 1600,
        'dias_germinacion': 0,
        'dias_hasta_cosecha': 1095,  # 3 años primera cosecha
        'ciclos_por_anio': 1,
        'frecuencia_riego_dias': 7,
        'litros_agua_por_planta_dia': Decimal('80.0'),
        'requiere_riego_constante': False,
        'rendimiento_promedio_hectarea': Decimal('12'),  # toneladas
        'precio_mercado_promedio': Decimal('2.50'),  # USD por kg
        'demanda_mercado': 'MUY_ALTA',
        'nivel_dificultad': 'MODERADO',
        'certificaciones_recomendadas': ['GlobalG.A.P.', 'Orgánico'],
        'permisos_requeridos_ecuador': ['Registro AGROCALIDAD', 'Certificado Fitosanitario'],
        'descripcion': 'Cultivo en expansión con alta demanda internacional',
        'plagas_comunes': ['Trips', 'Barrenador del tallo'],
        'enfermedades_comunes': ['Antracnosis', 'Phytophthora'],
        'compatibilidad_rotacion': []
    },
    {
        'nombre_cientifico': 'Theobroma cacao',
        'nombre_comun': 'Cacao',
        'categoria': 'FRUTAS',
        'variedades': ['CCN-51', 'Nacional', 'Trinitario'],
        'ph_minimo': Decimal('5.5'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('7.0'),
        'ph_maximo': Decimal('7.5'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_ARCILLOSO', 'FRANCO_LIMOSO'],
        'temperatura_min': Decimal('21.0'),
        'temperatura_optima_min': Decimal('24.0'),
        'temperatura_optima_max': Decimal('28.0'),
        'temperatura_max': Decimal('32.0'),
        'altitud_minima': 0,
        'altitud_maxima': 800,
        'precipitacion_anual_min': 1500,
        'precipitacion_anual_max': 3000,
        'dias_germinacion': 15,
        'dias_hasta_cosecha': 1460,  # 4 años
        'ciclos_por_anio': 2,
        'frecuencia_riego_dias': 5,
        'litros_agua_por_planta_dia': Decimal('30.0'),
        'requiere_riego_constante': True,
        'rendimiento_promedio_hectarea': Decimal('0.8'),  # toneladas
        'precio_mercado_promedio': Decimal('3.00'),  # USD por kg
        'demanda_mercado': 'ALTA',
        'nivel_dificultad': 'MODERADO',
        'certificaciones_recomendadas': ['Orgánico', 'Fair Trade', 'UTZ'],
        'permisos_requeridos_ecuador': ['Registro AGROCALIDAD'],
        'descripcion': 'Cacao fino de aroma ecuatoriano reconocido mundialmente',
        'plagas_comunes': ['Monilia', 'Escoba de bruja', 'Mazorca negra'],
        'enfermedades_comunes': ['Moniliasis', 'Phytophthora'],
        'compatibilidad_rotacion': []
    },
    
    # HORTALIZAS
    {
        'nombre_cientifico': 'Solanum lycopersicum',
        'nombre_comun': 'Tomate',
        'categoria': 'HORTALIZAS',
        'variedades': ['Cherry', 'Chonto', 'Riñón', 'Milano'],
        'ph_minimo': Decimal('5.5'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('6.8'),
        'ph_maximo': Decimal('7.5'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_ARENOSO'],
        'temperatura_min': Decimal('10.0'),
        'temperatura_optima_min': Decimal('18.0'),
        'temperatura_optima_max': Decimal('26.0'),
        'temperatura_max': Decimal('35.0'),
        'altitud_minima': 0,
        'altitud_maxima': 2800,
        'precipitacion_anual_min': 600,
        'precipitacion_anual_max': 1200,
        'dias_germinacion': 7,
        'dias_hasta_cosecha': 90,
        'ciclos_por_anio': 3,
        'frecuencia_riego_dias': 2,
        'litros_agua_por_planta_dia': Decimal('3.0'),
        'requiere_riego_constante': True,
        'rendimiento_promedio_hectarea': Decimal('60'),  # toneladas
        'precio_mercado_promedio': Decimal('0.80'),  # USD por kg
        'demanda_mercado': 'ALTA',
        'nivel_dificultad': 'MODERADO',
        'certificaciones_recomendadas': ['BPA', 'GlobalG.A.P.'],
        'permisos_requeridos_ecuador': ['Registro AGROCALIDAD'],
        'descripcion': 'Hortaliza de alto consumo nacional y regional',
        'plagas_comunes': ['Mosca blanca', 'Tuta absoluta', 'Trips'],
        'enfermedades_comunes': ['Tizón tardío', 'Fusarium', 'Virus mosaico'],
        'compatibilidad_rotacion': ['Lechuga', 'Cebolla', 'Zanahoria'],
    },
    {
        'nombre_cientifico': 'Lactuca sativa',
        'nombre_comun': 'Lechuga',
        'categoria': 'HORTALIZAS',
        'variedades': ['Crespa', 'Romana', 'Iceberg', 'Batavia'],
        'ph_minimo': Decimal('6.0'),
        'ph_optimo_min': Decimal('6.5'),
        'ph_optimo_max': Decimal('7.0'),
        'ph_maximo': Decimal('7.5'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_LIMOSO'],
        'temperatura_min': Decimal('7.0'),
        'temperatura_optima_min': Decimal('15.0'),
        'temperatura_optima_max': Decimal('20.0'),
        'temperatura_max': Decimal('24.0'),
        'altitud_minima': 1800,
        'altitud_maxima': 3200,
        'precipitacion_anual_min': 600,
        'precipitacion_anual_max': 900,
        'dias_germinacion': 5,
        'dias_hasta_cosecha': 60,
        'ciclos_por_anio': 6,
        'frecuencia_riego_dias': 2,
        'litros_agua_por_planta_dia': Decimal('1.0'),
        'requiere_riego_constante': True,
        'rendimiento_promedio_hectarea': Decimal('30'),  # toneladas
        'precio_mercado_promedio': Decimal('0.60'),  # USD por kg
        'demanda_mercado': 'ALTA',
        'nivel_dificultad': 'FACIL',
        'certificaciones_recomendadas': ['BPA'],
        'permisos_requeridos_ecuador': [],
        'descripcion': 'Cultivo de ciclo corto ideal para rotación',
        'plagas_comunes': ['Pulgones', 'Trips', 'Babosas'],
        'enfermedades_comunes': ['Mildiu', 'Esclerotinia'],
        'compatibilidad_rotacion': ['Tomate', 'Zanahoria', 'Brócoli'],
    },
    
    # TUBÉRCULOS
    {
        'nombre_cientifico': 'Solanum tuberosum',
        'nombre_comun': 'Papa',
        'categoria': 'TUBERCULOS',
        'variedades': ['Superchola', 'Única', 'Cecilia', 'Fripapa'],
        'ph_minimo': Decimal('5.0'),
        'ph_optimo_min': Decimal('5.5'),
        'ph_optimo_max': Decimal('6.5'),
        'ph_maximo': Decimal('7.0'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_ARENOSO'],
        'temperatura_min': Decimal('7.0'),
        'temperatura_optima_min': Decimal('12.0'),
        'temperatura_optima_max': Decimal('18.0'),
        'temperatura_max': Decimal('24.0'),
        'altitud_minima': 2400,
        'altitud_maxima': 3600,
        'precipitacion_anual_min': 500,
        'precipitacion_anual_max': 800,
        'dias_germinacion': 15,
        'dias_hasta_cosecha': 120,
        'ciclos_por_anio': 2,
        'frecuencia_riego_dias': 5,
        'litros_agua_por_planta_dia': Decimal('2.0'),
        'requiere_riego_constante': False,
        'rendimiento_promedio_hectarea': Decimal('25'),  # toneladas
        'precio_mercado_promedio': Decimal('0.45'),  # USD por kg
        'demanda_mercado': 'ALTA',
        'nivel_dificultad': 'MODERADO',
        'certificaciones_recomendadas': ['BPA'],
        'permisos_requeridos_ecuador': ['Semilla Certificada INIAP'],
        'descripcion': 'Alimento básico de la sierra ecuatoriana',
        'plagas_comunes': ['Gusano blanco', 'Polilla', 'Pulguilla'],
        'enfermedades_comunes': ['Tizón tardío', 'Rizoctonia', 'Virus PVY'],
        'compatibilidad_rotacion': ['Haba', 'Cebada', 'Avena'],
    },
    
    # GRANOS
    {
        'nombre_cientifico': 'Zea mays',
        'nombre_comun': 'Maíz',
        'categoria': 'GRANOS',
        'variedades': ['INIAP 551', 'INIAP 601', 'Híbrido DK-7088'],
        'ph_minimo': Decimal('5.5'),
        'ph_optimo_min': Decimal('6.0'),
        'ph_optimo_max': Decimal('7.0'),
        'ph_maximo': Decimal('8.0'),
        'texturas_compatibles': ['FRANCO', 'FRANCO_LIMOSO', 'FRANCO_ARCILLOSO'],
        'temperatura_min': Decimal('10.0'),
        'temperatura_optima_min': Decimal('20.0'),
        'temperatura_optima_max': Decimal('30.0'),
        'temperatura_max': Decimal('35.0'),
        'altitud_minima': 0,
        'altitud_maxima': 3200,
        'precipitacion_anual_min': 500,
        'precipitacion_anual_max': 1000,
        'dias_germinacion': 7,
        'dias_hasta_cosecha': 150,
        'ciclos_por_anio': 2,
        'frecuencia_riego_dias': 7,
        'litros_agua_por_planta_dia': Decimal('4.0'),
        'requiere_riego_constante': False,
        'rendimiento_promedio_hectarea': Decimal('5'),  # toneladas
        'precio_mercado_promedio': Decimal('0.35'),  # USD por kg
        'demanda_mercado': 'ALTA',
        'nivel_dificultad': 'FACIL',
        'certificaciones_recomendadas': [],
        'permisos_requeridos_ecuador': [],
        'descripcion': 'Cultivo tradicional de subsistencia y comercial',
        'plagas_comunes': ['Gusano cogollero', 'Gusano elotero'],
        'enfermedades_comunes': ['Mancha de asfalto', 'Pudrición del tallo'],
        'compatibilidad_rotacion': ['Fréjol', 'Haba'],
    },
]

cultivos_creados = 0
for cultivo_data in cultivos_data:
    cultivo, created = CatalogosCultivos.objects.get_or_create(
        nombre_comun=cultivo_data['nombre_comun'],
        defaults=cultivo_data
    )
    if created:
        cultivos_creados += 1
        print(f"  ✓ Creado: {cultivo.nombre_comun} ({cultivo.categoria})")
    else:
        print(f"    Existe: {cultivo.nombre_comun}")

print(f"\n✓ Total cultivos creados: {cultivos_creados}/{len(cultivos_data)}")

# ============================================================================
# PERMISOS NACIONALES ECUADOR
# ============================================================================
print("\n[2/2] Creando permisos nacionales de Ecuador...")

permisos_data = [
    # AGROCALIDAD - Fitosanitarios
    {
        'nombre_permiso': 'Registro de Productores',
        'codigo_permiso': 'AGRO-REG-PROD',
        'tipo_permiso': 'PRODUCCION',
        'entidad_emisora': 'AGROCALIDAD',
        'descripcion': 'Registro obligatorio para productores agrícolas que deseen comercializar sus productos',
        'requisitos': [
            'Cédula de identidad o RUC',
            'Escrituras de propiedad o contrato de arrendamiento',
            'Croquis de ubicación de la finca',
            'Plan de manejo de cultivo'
        ],
        'documentos_requeridos': [
            'Formulario de solicitud',
            'Copia de cédula',
            'Certificado de no adeudar al IESS',
            'Inspección técnica de la finca'
        ],
        'aplica_todo_cultivo': True,
        'tiempo_tramite_dias': 30,
        'vigencia_meses': 12,
        'costo_estimado': Decimal('0.00'),
        'url_tramite': 'https://www.agrocalidad.gob.ec/servicios/registro-de-productores/',
        'url_informacion': 'https://www.agrocalidad.gob.ec',
        'es_obligatorio': True
    },
    {
        'nombre_permiso': 'Certificado Fitosanitario de Exportación',
        'codigo_permiso': 'AGRO-CERT-FITO-EXP',
        'tipo_permiso': 'EXPORTACION',
        'entidad_emisora': 'AGROCALIDAD',
        'descripcion': 'Certificado que garantiza que los productos vegetales están libres de plagas y enfermedades',
        'requisitos': [
            'Registro de productor vigente',
            'Declaración de lote a exportar',
            'Inspección fitosanitaria favorable',
            'Certificado de fumigación (si aplica)'
        ],
        'documentos_requeridos': [
            'Solicitud de certificación',
            'Factura comercial',
            'Lista de empaque',
            'Resultados de análisis de laboratorio'
        ],
        'aplica_todo_cultivo': False,
        'tiempo_tramite_dias': 3,
        'vigencia_meses': 1,
        'costo_estimado': Decimal('25.00'),
        'url_tramite': 'https://www.agrocalidad.gob.ec/certificado-fitosanitario/',
        'es_obligatorio': True
    },
    {
        'nombre_permiso': 'Registro de Predios con Código Único',
        'codigo_permiso': 'AGRO-COD-UNICO',
        'tipo_permiso': 'PRODUCCION',
        'entidad_emisora': 'AGROCALIDAD',
        'descripcion': 'Código único de identificación de predios agrícolas para trazabilidad',
        'requisitos': [
            'Registro de productor',
            'Coordenadas geográficas del predio',
            'Área cultivada',
            'Tipo de cultivo'
        ],
        'documentos_requeridos': [
            'Formulario de registro',
            'Croquis de ubicación',
            'Coordenadas GPS'
        ],
        'aplica_todo_cultivo': False,  # Solo exportación
        'tiempo_tramite_dias': 15,
        'vigencia_meses': 12,
        'costo_estimado': Decimal('0.00'),
        'url_tramite': 'https://www.agrocalidad.gob.ec',
        'observaciones': 'Obligatorio para productos de exportación como banano, flores, cacao',
        'es_obligatorio': False
    },
    {
        'nombre_permiso': 'Certificado de Aplicación BPA',
        'codigo_permiso': 'AGRO-BPA',
        'tipo_permiso': 'PRODUCCION',
        'entidad_emisora': 'AGROCALIDAD',
        'descripcion': 'Certificación de Buenas Prácticas Agrícolas',
        'requisitos': [
            'Implementación de sistema BPA',
            'Capacitación de personal',
            'Registros de aplicación de agroquímicos',
            'Manejo de residuos'
        ],
        'documentos_requeridos': [
            'Manual de BPA implementado',
            'Registros de trazabilidad',
            'Certificados de capacitación',
            'Evidencia de auditoría interna'
        ],
        'aplica_todo_cultivo': True,
        'tiempo_tramite_dias': 60,
        'vigencia_meses': 24,
        'costo_estimado': Decimal('150.00'),
        'url_tramite': 'https://www.agrocalidad.gob.ec/certificacion-bpa/',
        'es_obligatorio': False
    },
    
    # MAG - Ministerio de Agricultura
    {
        'nombre_permiso': 'Registro de Empacadora',
        'codigo_permiso': 'MAG-REG-EMPAC',
        'tipo_permiso': 'COMERCIALIZACION',
        'entidad_emisora': 'MAG',
        'descripcion': 'Registro de instalaciones de empaque de productos agrícolas',
        'requisitos': [
            'Instalaciones adecuadas',
            'Sistema de trazabilidad',
            'Personal capacitado',
            'Equipos calibrados'
        ],
        'documentos_requeridos': [
            'Planos de la empacadora',
            'Permiso de funcionamiento municipal',
            'Certificado de calibración de equipos',
            'Plan de manejo de residuos'
        ],
        'aplica_todo_cultivo': False,
        'tiempo_tramite_dias': 45,
        'vigencia_meses': 24,
        'costo_estimado': Decimal('200.00'),
        'url_tramite': 'https://www.agricultura.gob.ec',
        'es_obligatorio': False
    },
    
    # MAATE - Ministerio del Ambiente
    {
        'nombre_permiso': 'Licencia Ambiental Categoría 4',
        'codigo_permiso': 'MAATE-LIC-AMB-4',
        'tipo_permiso': 'AMBIENTAL',
        'entidad_emisora': 'MAATE',
        'descripcion': 'Licencia ambiental para actividades agrícolas de bajo impacto',
        'requisitos': [
            'Ficha ambiental',
            'Plan de manejo ambiental',
            'Coordenadas del predio',
            'Área de cultivo'
        ],
        'documentos_requeridos': [
            'Formulario único ambiental',
            'Certificado de intersección',
            'Plan de manejo de desechos',
            'Estudio de impacto ambiental (según categoría)'
        ],
        'aplica_todo_cultivo': False,
        'tiempo_tramite_dias': 90,
        'vigencia_meses': 60,
        'costo_estimado': Decimal('500.00'),
        'url_tramite': 'https://www.ambiente.gob.ec',
        'observaciones': 'Requerido para fincas mayores a 20 hectáreas o en zonas protegidas',
        'es_obligatorio': False
    },
    {
        'nombre_permiso': 'Permiso de Uso de Agua para Riego',
        'codigo_permiso': 'MAATE-AGUA-RIEGO',
        'tipo_permiso': 'USO_AGUA',
        'entidad_emisora': 'MAATE',
        'descripcion': 'Autorización para uso de fuentes hídricas para riego agrícola',
        'requisitos': [
            'Estudio hidrológico',
            'Coordenadas de captación',
            'Caudal requerido',
            'Sistema de riego implementado'
        ],
        'documentos_requeridos': [
            'Solicitud de concesión',
            'Estudio técnico',
            'Certificado de no afectación a terceros',
            'Plan de uso eficiente del agua'
        ],
        'aplica_todo_cultivo': True,
        'tiempo_tramite_dias': 120,
        'vigencia_meses': 120,  # 10 años
        'costo_estimado': Decimal('150.00'),
        'url_tramite': 'https://www.ambiente.gob.ec',
        'es_obligatorio': True
    },
    
    # ARCSA
    {
        'nombre_permiso': 'Notificación Sanitaria',
        'codigo_permiso': 'ARCSA-NOTIF-SAN',
        'tipo_permiso': 'COMERCIALIZACION',
        'entidad_emisora': 'ARCSA',
        'descripcion': 'Notificación sanitaria para productos procesados',
        'requisitos': [
            'Registro de establecimiento',
            'Fichas técnicas de productos',
            'Análisis de laboratorio',
            'BPM implementadas'
        ],
        'documentos_requeridos': [
            'Formulario de notificación',
            'Certificado de BPM',
            'Análisis microbiológicos',
            'Diseño de etiqueta'
        ],
        'aplica_todo_cultivo': False,
        'tiempo_tramite_dias': 30,
        'vigencia_meses': 60,
        'costo_estimado': Decimal('208.00'),
        'url_tramite': 'https://www.controlsanitario.gob.ec',
        'observaciones': 'Solo para productos procesados o empacados',
        'es_obligatorio': False
    },
    
    # SENADI - Exportación
    {
        'nombre_permiso': 'Código de Exportador',
        'codigo_permiso': 'SENADI-COD-EXP',
        'tipo_permiso': 'EXPORTACION',
        'entidad_emisora': 'SENADI',
        'descripcion': 'Registro como exportador ante el Servicio Nacional de Aduanas',
        'requisitos': [
            'RUC activo',
            'Certificado bancario',
            'Registro en VUE',
            'Correo electrónico'
        ],
        'documentos_requeridos': [
            'Formulario de registro',
            'Copia de RUC',
            'Certificado de cuenta bancaria',
            'Copia de cédula del representante legal'
        ],
        'aplica_todo_cultivo': False,
        'tiempo_tramite_dias': 5,
        'vigencia_meses': 9999,  # Indefinido
        'costo_estimado': Decimal('0.00'),
        'url_tramite': 'https://www.aduana.gob.ec',
        'es_obligatorio': True
    },
    
    # GAD Municipal
    {
        'nombre_permiso': 'Permiso de Funcionamiento Municipal',
        'codigo_permiso': 'GAD-PERM-FUNC',
        'tipo_permiso': 'PRODUCCION',
        'entidad_emisora': 'GAD_MUNICIPAL',
        'descripcion': 'Permiso de funcionamiento para instalaciones agrícolas',
        'requisitos': [
            'Licencia metropolitana única',
            'Permiso de bomberos',
            'Uso de suelo compatible',
            'Pago de patente'
        ],
        'documentos_requeridos': [
            'Formulario municipal',
            'Certificado de uso de suelo',
            'Inspección de bomberos',
            'Copia de RUC'
        ],
        'aplica_todo_cultivo': False,
        'tiempo_tramite_dias': 15,
        'vigencia_meses': 12,
        'costo_estimado': Decimal('50.00'),
        'url_tramite': 'Varía según cantón',
        'observaciones': 'Requerido para empacadoras, centros de acopio, procesamiento',
        'es_obligatorio': False
    },
]

permisos_creados = 0
for permiso_data in permisos_data:
    permiso, created = PermisosNacionalesEcuador.objects.get_or_create(
        codigo_permiso=permiso_data['codigo_permiso'],
        defaults=permiso_data
    )
    if created:
        permisos_creados += 1
        print(f"  ✓ Creado: {permiso.nombre_permiso} ({permiso.entidad_emisora})")
    else:
        print(f"    Existe: {permiso.nombre_permiso}")

print(f"\n✓ Total permisos creados: {permisos_creados}/{len(permisos_data)}")

# ============================================================================
# ASOCIAR PERMISOS CON CULTIVOS
# ============================================================================
print("\n[3/3] Asociando permisos con cultivos específicos...")

# Permisos específicos para flores de exportación
permiso_codigo_unico = PermisosNacionalesEcuador.objects.get(codigo_permiso='AGRO-COD-UNICO')
permiso_cert_fito = PermisosNacionalesEcuador.objects.get(codigo_permiso='AGRO-CERT-FITO-EXP')
permiso_exportador = PermisosNacionalesEcuador.objects.get(codigo_permiso='SENADI-COD-EXP')

cultivos_exportacion = CatalogosCultivos.objects.filter(
    nombre_comun__in=['Rosa', 'Gypsophila', 'Banano', 'Cacao', 'Aguacate Hass']
)
for cultivo in cultivos_exportacion:
    permiso_codigo_unico.cultivos_aplicables.add(cultivo)
    permiso_cert_fito.cultivos_aplicables.add(cultivo)
    permiso_exportador.cultivos_aplicables.add(cultivo)
    print(f"  ✓ Asociados permisos de exportación a: {cultivo.nombre_comun}")

# Permiso de semilla certificada para papa
permiso_semilla = PermisosNacionalesEcuador.objects.filter(
    nombre_permiso__icontains='Semilla'
).first()
if permiso_semilla:
    papa = CatalogosCultivos.objects.filter(nombre_comun='Papa').first()
    if papa:
        permiso_semilla.cultivos_aplicables.add(papa)

print("\n" + "="*80)
print("RESUMEN")
print("="*80)
print(f"✓ Cultivos en catálogo: {CatalogosCultivos.objects.count()}")
print(f"✓ Permisos nacionales: {PermisosNacionalesEcuador.objects.count()}")
print("\n" + "="*80)
print("DATOS DE PLANIFICACIÓN POBLADOS EXITOSAMENTE")
print("="*80)
