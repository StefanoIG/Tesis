#!/usr/bin/env python
import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

# Get token
print("Getting JWT token...")
token_response = requests.post(
    f'{BASE_URL}/auth/token/',
    json={'username': 'Stefano', 'password': 'Paladins#23'}
)
token = token_response.json()['access']
headers = {'Authorization': f'Bearer {token}'}
print(f"✓ Token obtained: {token[:50]}...")

# Get empresas
print("\n=== GET /usuarios/empresas/ ===")
empresas = requests.get(f'{BASE_URL}/usuarios/empresas/', headers=headers).json()
print(f"Total empresas: {empresas['count']}")
if empresas['results']:
    empresa_id = empresas['results'][0]['id']
    print(f"Primera empresa: {empresas['results'][0]['nombre']}")
else:
    print("No empresas found!")
    empresa_id = None

# Create finca
if empresa_id:
    print("\n=== POST /usuarios/fincas/ ===")
    import uuid
    finca_data = {
        'nombre': f'Finca Test {uuid.uuid4().hex[:6]}',
        'codigo_finca': f'FINCA{uuid.uuid4().hex[:8].upper()}',
        'empresa': empresa_id,
        'direccion': 'Km 5 Via Test',
        'ciudad': 'Bogota',
        'coordenadas_latitud': 5.3833,
        'coordenadas_longitud': -73.3667,
        'tamaño_hectareas': 75.50
    }
    finca_response = requests.post(f'{BASE_URL}/usuarios/fincas/', json=finca_data, headers=headers)
    if finca_response.status_code == 201:
        finca = finca_response.json()
        print(f"✓ Finca created: {finca['nombre']} (ID: {finca['id']})")
        finca_id = finca['id']
    else:
        print(f"✗ Error creating finca: {finca_response.status_code}")
        try:
            print(json.dumps(finca_response.json(), indent=2, ensure_ascii=False))
        except:
            print(finca_response.text)
        finca_id = None
else:
    finca_id = None

# Create notificacion
print("\n=== POST /notificaciones/notificaciones/ ===")
notif_data = {
    'titulo': 'Prueba de Notificacion',
    'cuerpo': 'Este es un mensaje de prueba del sistema',
    'tipo_notificacion': 'INFORMATIVO',
    'usuario': 2  # Stefano's user ID
}
notif_response = requests.post(f'{BASE_URL}/notificaciones/notificaciones/', json=notif_data, headers=headers)
if notif_response.status_code == 201:
    notif = notif_response.json()
    print(f"✓ Notificacion created: {notif['titulo']}")
else:
    print(f"✗ Error creating notificacion: {notif_response.status_code}")
    try:
        print(json.dumps(notif_response.json(), indent=2, ensure_ascii=False))
    except:
        print(notif_response.text)

# Test GET without auth
print("\n=== Test unauthorized access ===")
no_auth = requests.get(f'{BASE_URL}/usuarios/empresas/')
print(f"GET without token status: {no_auth.status_code} (should be 401)")

# Test other modules
print("\n=== Testing other modules ===")
modules = [
    'usuarios/empresas/',
    'usuarios/fincas/',
    'logistica/envios/',
    'reportes/reportes/',
    'alertas/alertas/',
    'documentos/documentos/',
    'notificaciones/notificaciones/',
    'trazabilidad/lotes/',
    'procesamiento/procesos-procesamiento/',
]
for module in modules:
    response = requests.get(f'{BASE_URL}/{module}', headers=headers)
    status = '✓' if response.status_code == 200 else '✗'
    print(f"{status} GET /{module}: {response.status_code}")

