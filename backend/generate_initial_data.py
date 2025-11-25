"""
Script para generar datos iniciales de prueba para el sistema de trazabilidad agroindustrial.
Ejecutar: python manage.py shell < generate_initial_data.py
O bien: python generate_initial_data.py (si se configura como standalone)
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from django.utils import timezone

from django.contrib.auth import get_user_model
from apps.autenticacion.models import Roles, UsuariosRoles
from apps.usuarios.models import Empresas, Fincas, UsuariosEmpresas, Permisos, RolesPermisos
from apps.roles_permisos.models import (
    Roles as RolesExtendidos, 
    Permisos as PermisosExtendidos,
    RolesPermisos as RolesPermisosExtendidos
)
from apps.trazabilidad.models import (
    Productos, Lotes, HistorialEstadosLote,
    EventosTrazabilidad, TiposEventosTrazabilidad
)
from apps.procesamiento.models import (
    ProcesosProcesamiento, InspeccionesCalidad,
    CertificacionesEstandares, ResultadosAnalisisLaboratorio
)
from apps.logistica.models import Vehiculos, Conductores, Ubicaciones, Transportes
from apps.certificaciones.models import (
    Certificaciones, CertificacionesProductores,
    CertificacionesLotes, RequisitosCumplimiento
)
from apps.sensores.models import DispositivosSensores, LecturasSensores
from apps.clientes.models import Clientes, Ventas, DetallesVenta

Usuarios = get_user_model()

print("="*80)
print("GENERANDO DATOS INICIALES DE PRUEBA")
print("="*80)

# ============================================================================
# 1. USUARIOS Y AUTENTICACIÓN
# ============================================================================
print("\n[1/12] Creando usuarios y roles básicos...")

# Crear roles básicos
roles_data = [
    {'nombre_rol': 'Administrador', 'descripcion': 'Acceso total al sistema'},
    {'nombre_rol': 'Gerente', 'descripcion': 'Gestión de empresa y fincas'},
    {'nombre_rol': 'Supervisor', 'descripcion': 'Supervisión de operaciones'},
    {'nombre_rol': 'Operador Campo', 'descripcion': 'Operaciones en campo'},
    {'nombre_rol': 'Operador Planta', 'descripcion': 'Operaciones en planta'},
    {'nombre_rol': 'Auditor', 'descripcion': 'Solo lectura para auditoría'},
    {'nombre_rol': 'Cliente', 'descripcion': 'Acceso a información de trazabilidad'},
]

roles_creados = {}
for rol_data in roles_data:
    rol, created = Roles.objects.get_or_create(
        nombre_rol=rol_data['nombre_rol'],
        defaults=rol_data
    )
    roles_creados[rol.nombre_rol] = rol
    print(f"  {'✓ Creado' if created else '  Existe'}: {rol.nombre_rol}")

# Crear usuarios de prueba
usuarios_data = [
    {
        'username': 'admin',
        'email': 'admin@agrotrace.com',
        'nombre_completo': 'Administrador Sistema',
        'password': 'Admin123!',
        'rol': 'Administrador',
        'is_staff': True,
        'is_superuser': True
    },
    {
        'username': 'gerente',
        'email': 'gerente@fincatest.com',
        'nombre_completo': 'Juan Pérez',
        'password': 'Gerente123!',
        'rol': 'Gerente',
        'telefono': '+593987654321'
    },
    {
        'username': 'supervisor',
        'email': 'supervisor@fincatest.com',
        'nombre_completo': 'María González',
        'password': 'Super123!',
        'rol': 'Supervisor',
        'telefono': '+593987654322'
    },
    {
        'username': 'operador1',
        'email': 'operador1@fincatest.com',
        'nombre_completo': 'Carlos Rodríguez',
        'password': 'Oper123!',
        'rol': 'Operador Campo',
        'telefono': '+593987654323'
    },
    {
        'username': 'auditor',
        'email': 'auditor@external.com',
        'nombre_completo': 'Ana Martínez',
        'password': 'Audit123!',
        'rol': 'Auditor',
        'telefono': '+593987654324'
    },
]

usuarios_creados = {}
for user_data in usuarios_data:
    rol_nombre = user_data.pop('rol')
    password = user_data.pop('password')
    username = user_data.pop('username')
    
    usuario, created = Usuarios.objects.get_or_create(
        username=username,
        defaults={**user_data, 'username': username}
    )
    
    if created:
        usuario.set_password(password)
        usuario.save()
        
        # Asignar rol
        UsuariosRoles.objects.get_or_create(
            usuario=usuario,
            rol=roles_creados[rol_nombre]
        )
        print(f"  ✓ Usuario creado: {usuario.email} ({rol_nombre})")
    else:
        print(f"    Existe: {usuario.email}")
    
    usuarios_creados[usuario.email] = usuario

# ============================================================================
# 2. EMPRESAS Y FINCAS
# ============================================================================
print("\n[2/12] Creando empresas y fincas...")

empresas_data = [
    {
        'nombre': 'AgroTech Solutions S.A.',
        'tipo_empresa': 'PRODUCTOR',
        'registro_nacional': '1792345678001',
        'direccion': 'Av. Principal 123, Quito',
        'ciudad': 'Quito',
        'pais': 'Ecuador',
        'telefono': '+593234567890',
        'email': 'contacto@agrotech.ec',
    },
    {
        'nombre': 'Frutas del Valle Ltda.',
        'tipo_empresa': 'EXPORTADOR',
        'registro_nacional': '1798765432001',
        'direccion': 'Km 15 Vía a la Costa',
        'ciudad': 'Guayaquil',
        'pais': 'Ecuador',
        'telefono': '+593242345678',
        'email': 'info@frutasdelvalle.ec',
    }
]

empresas_creadas = {}
for emp_data in empresas_data:
    empresa, created = Empresas.objects.get_or_create(
        registro_nacional=emp_data['registro_nacional'],
        defaults=emp_data
    )
    empresas_creadas[empresa.nombre] = empresa
    print(f"  {'✓ Creado' if created else '  Existe'}: {empresa.nombre}")

# Asociar usuarios con empresas
UsuariosEmpresas.objects.get_or_create(
    usuario=usuarios_creados['gerente@fincatest.com'],
    empresa=empresas_creadas['AgroTech Solutions S.A.'],
    defaults={'es_responsable': True}
)
UsuariosEmpresas.objects.get_or_create(
    usuario=usuarios_creados['supervisor@fincatest.com'],
    empresa=empresas_creadas['AgroTech Solutions S.A.']
)

# Crear fincas
fincas_data = [
    {
        'empresa': 'AgroTech Solutions S.A.',
        'nombre': 'Finca San José',
        'codigo_finca': 'FSJ001',
        'direccion': 'Km 25 Vía Quito-Cayambe',
        'ciudad': 'Cayambe',
        'coordenadas_latitud': 0.0333,
        'coordenadas_longitud': -78.1500,
        'tamaño_hectareas': Decimal('150.50'),
    },
    {
        'empresa': 'AgroTech Solutions S.A.',
        'nombre': 'Finca El Rosal',
        'codigo_finca': 'FER002',
        'direccion': 'Sector Tabacundo',
        'ciudad': 'Pedro Moncayo',
        'coordenadas_latitud': 0.0167,
        'coordenadas_longitud': -78.2167,
        'tamaño_hectareas': Decimal('85.25'),
    },
    {
        'empresa': 'Frutas del Valle Ltda.',
        'nombre': 'Hacienda Tropical',
        'codigo_finca': 'HT003',
        'direccion': 'Km 45 Vía Guayaquil-Daule',
        'ciudad': 'Daule',
        'coordenadas_latitud': -1.8667,
        'coordenadas_longitud': -79.9833,
        'tamaño_hectareas': Decimal('200.00'),
    }
]

fincas_creadas = {}
for finca_data in fincas_data:
    empresa_nombre = finca_data.pop('empresa')
    finca, created = Fincas.objects.get_or_create(
        codigo_finca=finca_data['codigo_finca'],
        defaults={**finca_data, 'empresa': empresas_creadas[empresa_nombre]}
    )
    fincas_creadas[finca.nombre] = finca
    print(f"  {'✓ Creado' if created else '  Existe'}: {finca.nombre}")

# ============================================================================
# 3. UBICACIONES (LOGÍSTICA)
# ============================================================================
print("\n[3/12] Creando ubicaciones...")

ubicaciones_data = [
    {
        'empresa': 'AgroTech Solutions S.A.',
        'nombre': 'Almacén Central Quito',
        'tipo_ubicacion': 'ALMACEN',
        'latitud': Decimal('0.2000'),
        'longitud': Decimal('-78.5000'),
        'direccion': 'Parque Industrial Quito Norte',
        'ciudad': 'Quito',
    },
    {
        'empresa': 'AgroTech Solutions S.A.',
        'nombre': 'Planta de Empaque',
        'tipo_ubicacion': 'PLANTA',
        'latitud': Decimal('0.0500'),
        'longitud': Decimal('-78.1600'),
        'direccion': 'Zona Industrial Cayambe',
        'ciudad': 'Cayambe',
    },
    {
        'empresa': 'Frutas del Valle Ltda.',
        'nombre': 'Almacén Guayaquil',
        'tipo_ubicacion': 'ALMACEN',
        'latitud': Decimal('-2.1500'),
        'longitud': Decimal('-79.9000'),
        'direccion': 'Av. del Puerto',
        'ciudad': 'Guayaquil',
    },
]

ubicaciones_creadas = {}
for ubi_data in ubicaciones_data:
    empresa_nombre = ubi_data.pop('empresa')
    ubi, created = Ubicaciones.objects.get_or_create(
        nombre=ubi_data['nombre'],
        empresa=empresas_creadas[empresa_nombre],
        defaults={**ubi_data, 'empresa': empresas_creadas[empresa_nombre]}
    )
    ubicaciones_creadas[ubi.nombre] = ubi
    print(f"  {'✓ Creado' if created else '  Existe'}: {ubi.nombre}")

# ============================================================================
# 4. PRODUCTOS
# ============================================================================
print("\n[4/12] Creando productos...")

productos_data = [
    {
        'nombre': 'Rosa Roja Freedom',
        'tipo_producto': 'PROCESADO',
        'descripcion': 'Rosa roja variedad Freedom, tallo largo',
        'unidad_medida': 'Tallos',
    },
    {
        'nombre': 'Rosa Blanca Vendela',
        'tipo_producto': 'PROCESADO',
        'descripcion': 'Rosa blanca variedad Vendela',
        'unidad_medida': 'Tallos',
    },
    {
        'nombre': 'Banano Cavendish',
        'tipo_producto': 'FRUTA',
        'descripcion': 'Banano variedad Cavendish premium',
        'unidad_medida': 'Cajas',
    },
    {
        'nombre': 'Aguacate Hass',
        'tipo_producto': 'FRUTA',
        'descripcion': 'Aguacate variedad Hass',
        'unidad_medida': 'kg',
    },
]

productos_creados = {}
for prod_data in productos_data:
    prod, created = Productos.objects.get_or_create(
        nombre=prod_data['nombre'],
        defaults=prod_data
    )
    productos_creados[prod.nombre] = prod
    print(f"  {'✓ Creado' if created else '  Existe'}: {prod.nombre}")

# ============================================================================
# 5. LOTES
# ============================================================================
print("\n[5/12] Creando lotes...")

lotes_data = [
    {
        'producto': 'Rosa Roja Freedom',
        'codigo_lote': 'LOTE-2024-001',
        'cantidad': Decimal('5000'),
        'unidad_medida': 'Tallos',
        'fecha_produccion': datetime.now() - timedelta(days=5),
        'estado': 'PROCESAMIENTO',
        'nombre_ubicacion_origen': 'Finca San José - Cayambe',
        'latitud_origen': Decimal('0.0333'),
        'longitud_origen': Decimal('-78.1500'),
    },
    {
        'producto': 'Rosa Blanca Vendela',
        'codigo_lote': 'LOTE-2024-002',
        'cantidad': Decimal('3000'),
        'unidad_medida': 'Tallos',
        'fecha_produccion': datetime.now() - timedelta(days=3),
        'estado': 'PRODUCCION',
        'nombre_ubicacion_origen': 'Finca El Rosal - Pedro Moncayo',
        'latitud_origen': Decimal('0.0167'),
        'longitud_origen': Decimal('-78.2167'),
    },
    {
        'producto': 'Banano Cavendish',
        'codigo_lote': 'LOTE-2024-003',
        'cantidad': Decimal('500'),
        'unidad_medida': 'Cajas',
        'fecha_produccion': datetime.now() - timedelta(days=2),
        'estado': 'ALMACENADO',
        'nombre_ubicacion_origen': 'Hacienda Tropical - Daule',
        'latitud_origen': Decimal('-1.8667'),
        'longitud_origen': Decimal('-79.9833'),
    },
]

lotes_creados = {}
for lote_data in lotes_data:
    producto_nombre = lote_data.pop('producto')
    
    lote, created = Lotes.objects.get_or_create(
        codigo_lote=lote_data['codigo_lote'],
        defaults={
            **lote_data,
            'producto': productos_creados[producto_nombre],
        }
    )
    lotes_creados[lote.codigo_lote] = lote
    print(f"  {'✓ Creado' if created else '  Existe'}: {lote.codigo_lote}")

# ============================================================================
# 6. CERTIFICACIONES
# ============================================================================
print("\n[6/12] Creando certificaciones...")

certificaciones_data = [
    {
        'nombre': 'GlobalG.A.P.',
        'codigo': 'GGAP',
        'tipo_certificacion': 'BPA',
        'entidad_emisora': 'FoodPLUS GmbH',
        'alcance': 'INTERNACIONAL',
        'descripcion': 'Certificación de Buenas Prácticas Agrícolas',
        'requisitos_generales': {
            'documentos': ['Política de inocuidad', 'Plan de manejo integrado de plagas'],
            'auditorias_anuales': True
        },
        'vigencia_anios': 1,
    },
    {
        'nombre': 'Rainforest Alliance',
        'codigo': 'RA',
        'tipo_certificacion': 'AMBIENTAL',
        'entidad_emisora': 'Rainforest Alliance',
        'alcance': 'INTERNACIONAL',
        'descripcion': 'Certificación de sostenibilidad ambiental y social',
        'requisitos_generales': {
            'criterios': ['Conservación ecosistemas', 'Bienestar trabajadores']
        },
        'vigencia_anios': 3,
    },
    {
        'nombre': 'Fair Trade',
        'codigo': 'FT',
        'tipo_certificacion': 'COMERCIO_JUSTO',
        'entidad_emisora': 'FLO-CERT',
        'alcance': 'INTERNACIONAL',
        'descripcion': 'Comercio justo',
        'requisitos_generales': {
            'criterios': ['Precio mínimo garantizado', 'Prima social']
        },
        'vigencia_anios': 3,
    },
]

certificaciones_creadas = {}
for cert_data in certificaciones_data:
    cert, created = Certificaciones.objects.get_or_create(
        nombre=cert_data['nombre'],
        defaults=cert_data
    )
    certificaciones_creadas[cert.nombre] = cert
    print(f"  {'✓ Creado' if created else '  Existe'}: {cert.nombre}")

# Asignar certificaciones a empresas
cert_productores_data = [
    {
        'productor': 'AgroTech Solutions S.A.',
        'certificacion': 'GlobalG.A.P.',
        'numero_certificado': 'GGN-4063061234567',
        'fecha_emision': datetime.now() - timedelta(days=180),
        'fecha_expiracion': datetime.now() + timedelta(days=185),
        'estado': 'VIGENTE',
    },
    {
        'productor': 'Frutas del Valle Ltda.',
        'certificacion': 'Rainforest Alliance',
        'numero_certificado': 'RA-EC-2024-001',
        'fecha_emision': datetime.now() - timedelta(days=90),
        'fecha_expiracion': datetime.now() + timedelta(days=1005),
        'estado': 'VIGENTE',
    },
]

for cert_prod_data in cert_productores_data:
    productor_nombre = cert_prod_data.pop('productor')
    cert_nombre = cert_prod_data.pop('certificacion')
    
    cert_prod, created = CertificacionesProductores.objects.get_or_create(
        productor=empresas_creadas[productor_nombre],
        certificacion=certificaciones_creadas[cert_nombre],
        defaults=cert_prod_data
    )
    print(f"  {'✓ Asignado' if created else '  Existe'}: {cert_nombre} -> {productor_nombre}")

# ============================================================================
# 7. VEHÍCULOS Y CONDUCTORES
# ============================================================================
print("\n[7/12] Creando vehículos y conductores...")

vehiculos_data = [
    {
        'empresa': 'AgroTech Solutions S.A.',
        'placa': 'PBZ-1234',
        'tipo_vehiculo': 'CAMION',
        'marca': 'Chevrolet',
        'modelo': 'NPR',
        'año_fabricacion': 2022,
        'capacidad_kg': Decimal('3500.00'),
        'es_refrigerado': True,
        'temperatura_min': 2.0,
        'temperatura_max': 8.0,
    },
    {
        'empresa': 'Frutas del Valle Ltda.',
        'placa': 'GYE-5678',
        'tipo_vehiculo': 'CAMION',
        'marca': 'Hino',
        'modelo': 'Serie 300',
        'año_fabricacion': 2021,
        'capacidad_kg': Decimal('5000.00'),
        'es_refrigerado': True,
        'temperatura_min': 12.0,
        'temperatura_max': 15.0,
    },
]

vehiculos_creados = {}
for veh_data in vehiculos_data:
    empresa_nombre = veh_data.pop('empresa')
    veh, created = Vehiculos.objects.get_or_create(
        placa=veh_data['placa'],
        defaults={**veh_data, 'empresa': empresas_creadas[empresa_nombre]}
    )
    vehiculos_creados[veh.placa] = veh
    print(f"  {'✓ Creado' if created else '  Existe'}: {veh.placa}")

# Crear conductores
conductores_data = [
    {
        'usuario': 'operador1@fincatest.com',
        'empresa': 'AgroTech Solutions S.A.',
        'numero_licencia': 'EC-PIC-123456',
        'categoria_licencia': 'C',
        'fecha_vencimiento_licencia': datetime.now().date() + timedelta(days=730),
    },
]

for cond_data in conductores_data:
    usuario_email = cond_data.pop('usuario')
    empresa_nombre = cond_data.pop('empresa')
    
    cond, created = Conductores.objects.get_or_create(
        usuario=usuarios_creados[usuario_email],
        defaults={**cond_data, 'empresa': empresas_creadas[empresa_nombre]}
    )
    print(f"  {'✓ Creado' if created else '  Existe'}: Conductor {cond.usuario.nombre_completo}")

# ============================================================================
# 8. SENSORES IoT
# ============================================================================
print("\n[8/12] Creando dispositivos sensores...")

sensores_data = [
    {
        'finca': 'Finca San José',
        'ubicacion': 'Almacén Central Quito',
        'codigo_dispositivo': 'SENS-TEMP-001',
        'nombre': 'Sensor Temperatura Almacén Quito',
        'tipo_dispositivo': 'TEMPERATURA',
        'fabricante': 'DHT',
        'modelo': 'AM2302',
        'umbral_alerta_min': 2.0,
        'umbral_alerta_max': 8.0,
        'estado': 'ACTIVO',
    },
    {
        'finca': 'Finca San José',
        'ubicacion': 'Almacén Central Quito',
        'codigo_dispositivo': 'SENS-HUM-001',
        'nombre': 'Sensor Humedad Almacén Quito',
        'tipo_dispositivo': 'HUMEDAD',
        'fabricante': 'DHT',
        'modelo': 'AM2302',
        'umbral_alerta_min': 60.0,
        'umbral_alerta_max': 80.0,
        'estado': 'ACTIVO',
    },
]

sensores_creados = {}
for sens_data in sensores_data:
    finca_nombre = sens_data.pop('finca')
    ubicacion_nombre = sens_data.pop('ubicacion')
    
    sens, created = DispositivosSensores.objects.get_or_create(
        codigo_dispositivo=sens_data['codigo_dispositivo'],
        defaults={
            **sens_data,
            'finca': fincas_creadas[finca_nombre],
            'ubicacion': ubicaciones_creadas[ubicacion_nombre],
        }
    )
    sensores_creados[sens.codigo_dispositivo] = sens
    print(f"  {'✓ Creado' if created else '  Existe'}: {sens.codigo_dispositivo}")

# ============================================================================
# 9. CLIENTES
# ============================================================================
print("\n[9/12] Creando clientes...")

clientes_data = [
    {
        'nombre_comercial': 'FloraMax International',
        'tipo_cliente': 'MAYORISTA',
        'identificacion_fiscal': '1790123456001',
        'email': 'compras@floramax.com',
        'telefono': '+1234567890',
        'pais': 'Estados Unidos',
        'ciudad': 'Miami',
        'provincia_estado': 'Florida',
        'direccion': '1234 Ocean Drive, Miami, FL',
    },
    {
        'nombre_comercial': 'European Fruits GmbH',
        'tipo_cliente': 'MAYORISTA',
        'identificacion_fiscal': 'DE123456789',
        'email': 'orders@eurofruits.de',
        'telefono': '+49123456789',
        'pais': 'Alemania',
        'ciudad': 'Hamburgo',
        'provincia_estado': 'Hamburg',
        'direccion': 'Hafen Straße 45, Hamburg',
    },
]

clientes_creados = {}
for cli_data in clientes_data:
    cli, created = Clientes.objects.get_or_create(
        identificacion_fiscal=cli_data['identificacion_fiscal'],
        defaults=cli_data
    )
    clientes_creados[cli.nombre_comercial] = cli
    print(f"  {'✓ Creado' if created else '  Existe'}: {cli.nombre_comercial}")

# ============================================================================
# 10. TIPOS DE EVENTOS DE TRAZABILIDAD
# ============================================================================
print("\n[10/12] Creando tipos de eventos...")

tipos_eventos_data = [
    {
        'nombre': 'Cosecha',
        'categoria': 'PRODUCCION',
        'descripcion': 'Registro de cosecha de producto',
    },
    {
        'nombre': 'Empaque',
        'categoria': 'PROCESAMIENTO',
        'descripcion': 'Proceso de empaque',
    },
    {
        'nombre': 'Transporte',
        'categoria': 'TRANSPORTE',
        'descripcion': 'Inicio de transporte',
    },
    {
        'nombre': 'Control Calidad',
        'categoria': 'CALIDAD',
        'descripcion': 'Inspección de calidad',
    },
]

tipos_eventos_creados = {}
for tipo_data in tipos_eventos_data:
    tipo, created = TiposEventosTrazabilidad.objects.get_or_create(
        nombre=tipo_data['nombre'],
        defaults=tipo_data
    )
    tipos_eventos_creados[tipo.nombre] = tipo
    print(f"  {'✓ Creado' if created else '  Existe'}: {tipo.nombre}")

# ============================================================================
# 11. PERMISOS EXTENDIDOS (Sistema RBAC)
# ============================================================================
print("\n[11/12] Creando permisos extendidos...")

permisos_extendidos_data = [
    # Permisos de usuarios
    {'modulo': 'usuarios', 'recurso': 'empresa', 'tipo_permiso': 'LECTURA', 'codigo_permiso': 'usuarios.empresa.ver'},
    {'modulo': 'usuarios', 'recurso': 'empresa', 'tipo_permiso': 'ESCRITURA', 'codigo_permiso': 'usuarios.empresa.crear'},
    {'modulo': 'usuarios', 'recurso': 'empresa', 'tipo_permiso': 'ESCRITURA', 'codigo_permiso': 'usuarios.empresa.editar'},
    {'modulo': 'usuarios', 'recurso': 'empresa', 'tipo_permiso': 'ELIMINACION', 'codigo_permiso': 'usuarios.empresa.eliminar'},
    
    # Permisos de trazabilidad
    {'modulo': 'trazabilidad', 'recurso': 'lote', 'tipo_permiso': 'LECTURA', 'codigo_permiso': 'trazabilidad.lote.ver'},
    {'modulo': 'trazabilidad', 'recurso': 'lote', 'tipo_permiso': 'ESCRITURA', 'codigo_permiso': 'trazabilidad.lote.crear'},
    {'modulo': 'trazabilidad', 'recurso': 'lote', 'tipo_permiso': 'ESCRITURA', 'codigo_permiso': 'trazabilidad.lote.editar'},
    
    # Permisos de procesamiento
    {'modulo': 'procesamiento', 'recurso': 'orden', 'tipo_permiso': 'LECTURA', 'codigo_permiso': 'procesamiento.orden.ver'},
    {'modulo': 'procesamiento', 'recurso': 'orden', 'tipo_permiso': 'ESCRITURA', 'codigo_permiso': 'procesamiento.orden.crear'},
    
    # Permisos de logística
    {'modulo': 'logistica', 'recurso': 'transporte', 'tipo_permiso': 'LECTURA', 'codigo_permiso': 'logistica.transporte.ver'},
    {'modulo': 'logistica', 'recurso': 'transporte', 'tipo_permiso': 'ESCRITURA', 'codigo_permiso': 'logistica.transporte.crear'},
    
    # Permisos de reportes
    {'modulo': 'reportes', 'recurso': 'trazabilidad', 'tipo_permiso': 'LECTURA', 'codigo_permiso': 'reportes.trazabilidad.ver'},
    {'modulo': 'reportes', 'recurso': 'trazabilidad', 'tipo_permiso': 'ESPECIAL', 'codigo_permiso': 'reportes.trazabilidad.exportar'},
]

permisos_ext_creados = {}
for perm_data in permisos_extendidos_data:
    # Extraer la acción del código de permiso (última parte después del último punto)
    accion = perm_data['codigo_permiso'].split('.')[-1]
    perm, created = PermisosExtendidos.objects.get_or_create(
        codigo_permiso=perm_data['codigo_permiso'],
        defaults={
            'nombre_permiso': f"{perm_data['modulo'].title()} - {perm_data['recurso'].title()} - {accion.title()}",
            **perm_data
        }
    )
    permisos_ext_creados[perm.codigo_permiso] = perm
    if created:
        print(f"  ✓ Creado: {perm.codigo_permiso}")

# Crear roles extendidos
roles_ext_data = [
    {
        'nombre_rol': 'Admin Total',
        'codigo_rol': 'ADMIN_TOTAL',
        'descripcion': 'Acceso completo a todos los módulos',
        'nivel_acceso': 10,
        'permisos': [p.codigo_permiso for p in permisos_ext_creados.values()]
    },
    {
        'nombre_rol': 'Gerente Operativo',
        'codigo_rol': 'GERENTE_OPS',
        'descripcion': 'Gestión de trazabilidad y procesamiento',
        'nivel_acceso': 8,
        'permisos': [
            'trazabilidad.lote.ver', 'trazabilidad.lote.crear', 'trazabilidad.lote.editar',
            'procesamiento.orden.ver', 'procesamiento.orden.crear',
            'reportes.trazabilidad.ver', 'reportes.trazabilidad.exportar'
        ]
    },
]

for rol_data in roles_ext_data:
    permisos_codes = rol_data.pop('permisos')
    rol, created = RolesExtendidos.objects.get_or_create(
        nombre_rol=rol_data['nombre_rol'],
        defaults=rol_data
    )
    
    if created:
        # Asignar permisos al rol
        for perm_code in permisos_codes:
            if perm_code in permisos_ext_creados:
                RolesPermisosExtendidos.objects.get_or_create(
                    rol=rol,
                    permiso=permisos_ext_creados[perm_code]
                )
        print(f"  ✓ Rol extendido creado: {rol.nombre_rol} ({len(permisos_codes)} permisos)")

# ============================================================================
# 12. DATOS TRANSACCIONALES DE EJEMPLO
# ============================================================================
print("\n[12/12] Creando datos transaccionales...")

# Eventos de trazabilidad para los lotes
eventos_data = [
    {
        'lote': 'LOTE-2024-001',
        'tipo_evento': 'Cosecha',
        'descripcion': 'Cosecha de rosas en Finca San José',
        'usuario': 'operador1@fincatest.com',
    },
    {
        'lote': 'LOTE-2024-001',
        'tipo_evento': 'Empaque',
        'descripcion': 'Empaque en cajas de 25 tallos',
        'usuario': 'operador1@fincatest.com',
    },
    {
        'lote': 'LOTE-2024-002',
        'tipo_evento': 'Cosecha',
        'descripcion': 'Cosecha de rosas blancas',
        'usuario': 'operador1@fincatest.com',
    },
]

for evento_data in eventos_data:
    lote_codigo = evento_data.pop('lote')
    tipo_evento_nombre = evento_data.pop('tipo_evento')
    usuario_email = evento_data.pop('usuario')
    
    evento, created = EventosTrazabilidad.objects.get_or_create(
        lote=lotes_creados[lote_codigo],
        tipo_evento=tipos_eventos_creados[tipo_evento_nombre],
        usuario=usuarios_creados[usuario_email],
        defaults={
            **evento_data,
            'fecha_evento': timezone.now() - timedelta(days=1)
        }
    )
    if created:
        print(f"  ✓ Evento registrado: {tipo_evento_nombre} en {lote_codigo}")

# Historial de estados
for lote_codigo, lote in lotes_creados.items():
    HistorialEstadosLote.objects.get_or_create(
        lote=lote,
        estado_anterior='PRODUCCION',
        estado_nuevo=lote.estado,
        defaults={'motivo': 'Estado inicial del lote'}
    )
print(f"  ✓ {len(lotes_creados)} registros de historial de estados creados")

# Lecturas de sensores
import random
for i in range(24):  # 24 lecturas (últimas 24 horas)
    hora = timezone.now() - timedelta(hours=i)
    
    # Temperatura
    LecturasSensores.objects.create(
        dispositivo=sensores_creados['SENS-TEMP-001'],
        tipo_medicion='temperatura',
        valor=Decimal(str(round(random.uniform(4.0, 8.0), 2))),
        unidad_medida='°C',
        fecha_lectura=hora
    )
    
    # Humedad
    LecturasSensores.objects.create(
        dispositivo=sensores_creados['SENS-HUM-001'],
        tipo_medicion='humedad',
        valor=Decimal(str(round(random.uniform(60.0, 80.0), 2))),
        unidad_medida='%',
        fecha_lectura=hora
    )

print("  ✓ 48 lecturas de sensores creadas (últimas 24 horas)")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN DE DATOS CREADOS")
print("="*80)
print(f"✓ Usuarios: {Usuarios.objects.count()}")
print(f"✓ Roles básicos: {Roles.objects.count()}")
print(f"✓ Empresas: {Empresas.objects.count()}")
print(f"✓ Fincas: {Fincas.objects.count()}")
print(f"✓ Ubicaciones: {Ubicaciones.objects.count()}")
print(f"✓ Productos: {Productos.objects.count()}")
print(f"✓ Lotes: {Lotes.objects.count()}")
print(f"✓ Certificaciones: {Certificaciones.objects.count()}")
print(f"✓ Vehículos: {Vehiculos.objects.count()}")
print(f"✓ Sensores: {DispositivosSensores.objects.count()}")
print(f"✓ Lecturas sensores: {LecturasSensores.objects.count()}")
print(f"✓ Clientes: {Clientes.objects.count()}")
print(f"✓ Permisos extendidos: {PermisosExtendidos.objects.count()}")
print(f"✓ Roles extendidos: {RolesExtendidos.objects.count()}")
print(f"✓ Eventos trazabilidad: {EventosTrazabilidad.objects.count()}")
print(f"✓ Historial estados: {HistorialEstadosLote.objects.count()}")

print("\n" + "="*80)
print("CREDENCIALES DE ACCESO")
print("="*80)
print("\nAdministrador:")
print("  Email: admin@agrotrace.com")
print("  Password: Admin123!")
print("\nGerente:")
print("  Email: gerente@fincatest.com")
print("  Password: Gerente123!")
print("\nSupervisor:")
print("  Email: supervisor@fincatest.com")
print("  Password: Super123!")
print("\nOperador:")
print("  Email: operador1@fincatest.com")
print("  Password: Oper123!")
print("\nAuditor:")
print("  Email: auditor@external.com")
print("  Password: Audit123!")

print("\n" + "="*80)
print("DATOS INICIALES GENERADOS EXITOSAMENTE")
print("="*80)
