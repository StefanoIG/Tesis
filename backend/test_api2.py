#!/usr/bin/env python
"""
Comprehensive API Test Suite
Tests all endpoints of the Django REST Framework API
"""
import requests
import json
import uuid
from datetime import datetime

BASE_URL = 'http://localhost:8000/api/v1'

class APITester:
    def __init__(self):
        self.token = None
        self.headers = {}
        self.results = []
        self.test_ids = {}
        
    def log(self, status, endpoint, method, message):
        """Log test result"""
        symbol = "[OK]" if status == "PASS" else "[ERR]" if status == "FAIL" else "[INF]"
        print(f"{symbol:6} {method:6} {endpoint:50} {message}")
        self.results.append({
            "status": status,
            "method": method,
            "endpoint": endpoint,
            "message": message
        })
    
    def login(self):
        """Authenticate and get JWT token"""
        print("\n" + "="*80)
        print("AUTHENTICATION")
        print("="*80)
        
        try:
            response = requests.post(
                f'{BASE_URL}/auth/token/',
                json={'username': 'Stefano', 'password': 'Paladins#23'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['access']
                self.headers = {'Authorization': f'Bearer {self.token}'}
                user_info = data.get('usuario', {})
                self.log("PASS", "/auth/token/", "POST", 
                        f"Token obtained for user: {user_info.get('nombre_completo', 'Unknown')}")
                return True
            else:
                self.log("FAIL", "/auth/token/", "POST", f"Status {response.status_code}")
                return False
        except Exception as e:
            self.log("FAIL", "/auth/token/", "POST", str(e))
            return False
    
    def test_get(self, endpoint, description=""):
        """Test GET endpoint"""
        try:
            response = requests.get(f'{BASE_URL}{endpoint}', headers=self.headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', len(data) if isinstance(data, list) else 1)
                msg = f"{description} - {count} items"
                self.log("PASS", endpoint, "GET", msg)
                return response.json()
            else:
                self.log("FAIL", endpoint, "GET", f"Status {response.status_code}")
                return None
        except Exception as e:
            self.log("FAIL", endpoint, "GET", str(e))
            return None
    
    def test_post(self, endpoint, data, description=""):
        """Test POST endpoint"""
        try:
            response = requests.post(
                f'{BASE_URL}{endpoint}',
                json=data,
                headers=self.headers,
                timeout=5
            )
            if response.status_code in [200, 201]:
                result = response.json()
                item_id = result.get('id', 'N/A')
                msg = f"{description} - Created ID: {str(item_id)[:8]}..."
                self.log("PASS", endpoint, "POST", msg)
                return result
            else:
                error = response.json() if response.text else response.status_code
                self.log("FAIL", endpoint, "POST", f"Status {response.status_code}")
                return None
        except Exception as e:
            self.log("FAIL", endpoint, "POST", str(e))
            return None
    
    def test_get_detail(self, endpoint, item_id, description=""):
        """Test GET detail endpoint"""
        try:
            url = f'{endpoint}{item_id}/'
            response = requests.get(f'{BASE_URL}{url}', headers=self.headers, timeout=5)
            if response.status_code == 200:
                self.log("PASS", url, "GET", description)
                return response.json()
            else:
                self.log("FAIL", url, "GET", f"Status {response.status_code}")
                return None
        except Exception as e:
            self.log("FAIL", url, "GET", str(e))
            return None
    
    def test_put(self, endpoint, item_id, data, description=""):
        """Test PUT endpoint"""
        try:
            url = f'{endpoint}{item_id}/'
            response = requests.put(
                f'{BASE_URL}{url}',
                json=data,
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 200:
                self.log("PASS", url, "PUT", description)
                return response.json()
            else:
                self.log("FAIL", url, "PUT", f"Status {response.status_code}")
                return None
        except Exception as e:
            self.log("FAIL", url, "PUT", str(e))
            return None
    
    def test_delete(self, endpoint, item_id, description=""):
        """Test DELETE endpoint"""
        try:
            url = f'{endpoint}{item_id}/'
            response = requests.delete(f'{BASE_URL}{url}', headers=self.headers, timeout=5)
            if response.status_code in [200, 204]:
                self.log("PASS", url, "DELETE", description)
                return True
            else:
                self.log("FAIL", url, "DELETE", f"Status {response.status_code}")
                return False
        except Exception as e:
            self.log("FAIL", url, "DELETE", str(e))
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        if not self.login():
            print("Cannot proceed without authentication")
            return
        
        # USUARIOS MODULE
        print("\n" + "="*80)
        print("USUARIOS MODULE")
        print("="*80)
        
        # Empresas
        empresas = self.test_get('/usuarios/empresas/', 'Listar empresas')
        if empresas and empresas.get('results'):
            empresa_id = empresas['results'][0]['id']
            self.test_ids['empresa'] = empresa_id
            self.test_get_detail('/usuarios/empresas/', empresa_id, 'Ver detalle empresa')
        
        # Create empresa
        empresa_data = {
            'nombre': f'Empresa Test {uuid.uuid4().hex[:6]}',
            'tipo_empresa': 'PRODUCTOR',
            'email': f'test{uuid.uuid4().hex[:4]}@empresa.com',
            'ciudad': 'Bogota',
            'direccion': 'Calle Test 123'
        }
        new_empresa = self.test_post('/usuarios/empresas/', empresa_data, 'Crear empresa')
        if new_empresa:
            empresa_id = new_empresa['id']
            self.test_ids['empresa'] = empresa_id
            
            # Update empresa
            update_data = {'ciudad': 'Medellin'}
            self.test_put('/usuarios/empresas/', empresa_id, update_data, 'Actualizar empresa')
        
        # Fincas
        if 'empresa' in self.test_ids:
            fincas = self.test_get('/usuarios/fincas/', 'Listar fincas')
            
            # Create finca
            finca_data = {
                'nombre': f'Finca Test {uuid.uuid4().hex[:6]}',
                'codigo_finca': f'FINCA{uuid.uuid4().hex[:6].upper()}',
                'empresa': self.test_ids['empresa'],
                'direccion': 'Km 5 Vía Test',
                'ciudad': 'Bogota',
                'coordenadas_latitud': 4.7110,
                'coordenadas_longitud': -74.0055,
                'tamaño_hectareas': 50.00
            }
            new_finca = self.test_post('/usuarios/fincas/', finca_data, 'Crear finca')
            if new_finca:
                self.test_ids['finca'] = new_finca['id']
                self.test_get_detail('/usuarios/fincas/', new_finca['id'], 'Ver detalle finca')
        
        # Permisos
        self.test_get('/usuarios/permisos/', 'Listar permisos')
        
        # Usuarios por empresa
        self.test_get('/usuarios/usuarios-empresas/', 'Listar usuarios por empresa')
        
        # TRAZABILIDAD MODULE
        print("\n" + "="*80)
        print("TRAZABILIDAD MODULE")
        print("="*80)
        
        # Crear Producto primero
        producto_data = {
            'nombre': f'Producto {uuid.uuid4().hex[:6]}',
            'tipo_producto': 'FRUTA',
            'descripcion': 'Producto de prueba',
            'unidad_medida': 'kg'
        }
        new_producto = self.test_post('/trazabilidad/productos/', producto_data, 'Crear producto')
        if new_producto:
            self.test_ids['producto'] = new_producto['id']
        
        if 'finca' in self.test_ids:
            # Lotes
            lotes = self.test_get('/trazabilidad/lotes/', 'Listar lotes')
            
            # Create lote - ahora con producto
            if 'producto' in self.test_ids:
                lote_data = {
                    'codigo_lote': f'LOTE{uuid.uuid4().hex[:6].upper()}',
                    'producto': self.test_ids['producto'],
                    'cantidad': 100.00,
                    'unidad_medida': 'kg',
                    'fecha_produccion': datetime.now().isoformat(),
                    'estado': 'PRODUCCION'
                }
                new_lote = self.test_post('/trazabilidad/lotes/', lote_data, 'Crear lote')
                if new_lote:
                    self.test_ids['lote'] = new_lote['id']
        
        # Tipos de eventos - Create if not exists
        tipo_evento_data = {
            'nombre': 'SIEMBRA',
            'descripcion': 'Evento de siembra'
        }
        tipo_evento = self.test_post('/trazabilidad/tipos-eventos/', tipo_evento_data, 'Crear tipo de evento')
        if tipo_evento:
            self.test_ids['tipo_evento'] = tipo_evento['id']
        
        # Eventos de trazabilidad
        if 'lote' in self.test_ids:
            eventos = self.test_get(f'/trazabilidad/lotes/{self.test_ids["lote"]}/eventos/', 'Listar eventos de lote')
            
            # Create evento - must use tipo_evento ID
            if 'tipo_evento' in self.test_ids:
                evento_data = {
                    'tipo_evento': self.test_ids['tipo_evento'],
                    'descripcion': 'Siembra de semillas de tomate',
                    'fecha_evento': datetime.now().isoformat()
                }
                self.test_post(f'/trazabilidad/lotes/{self.test_ids["lote"]}/eventos/', evento_data, 'Crear evento')
        
        # LOGISTICA MODULE
        print("\n" + "="*80)
        print("LOGISTICA MODULE")
        print("="*80)
        
        # Vehiculos
        self.test_get('/logistica/vehiculos/', 'Listar vehículos')
        
        # Conductores
        self.test_get('/logistica/conductores/', 'Listar conductores')
        
        # Envios
        envios = self.test_get('/logistica/envios/', 'Listar envíos')
        
        # Create envio - solo si tenemos lote (que requiere producto)
        if 'lote' in self.test_ids and 'empresa' in self.test_ids:
            envio_data = {
                'lote': str(self.test_ids['lote']),
                'nombre_origen': 'Finca Origen',
                'nombre_destino': 'Destino Centro',
                'latitud_origen': 4.7110,
                'longitud_origen': -74.0055,
                'latitud_destino': 4.6097,
                'longitud_destino': -74.0817,
                'estado': 'PENDIENTE'
            }
            new_envio = self.test_post('/logistica/envios/', envio_data, 'Crear envío')
            if new_envio:
                self.test_ids['envio'] = new_envio['id']
        
        # PROCESAMIENTO MODULE
        print("\n" + "="*80)
        print("PROCESAMIENTO MODULE")
        print("="*80)
        
        # Procesos de procesamiento
        self.test_get('/procesamiento/procesos/', 'Listar procesos de procesamiento')
        
        # Inspecciones
        self.test_get('/procesamiento/inspecciones/', 'Listar inspecciones de calidad')
        
        # Certificaciones
        self.test_get('/procesamiento/certificaciones/', 'Listar certificaciones')
        
        # Análisis de laboratorio
        self.test_get('/procesamiento/analisis-laboratorio/', 'Listar análisis de laboratorio')
        
        # REPORTES MODULE
        print("\n" + "="*80)
        print("REPORTES MODULE")
        print("="*80)
        
        self.test_get('/reportes/reportes/', 'Listar reportes')
        
        # DOCUMENTOS MODULE
        print("\n" + "="*80)
        print("DOCUMENTOS MODULE")
        print("="*80)
        
        self.test_get('/documentos/documentos/', 'Listar documentos')
        self.test_get('/documentos/fotos/', 'Listar fotos de productos')
        
        # SINCRONIZACION MODULE
        print("\n" + "="*80)
        print("SINCRONIZACION MODULE")
        print("="*80)
        
        self.test_get('/sincronizacion/estados/', 'Listar estados de sincronización')
        self.test_get('/sincronizacion/conflictos/', 'Listar conflictos de sincronización')
        self.test_get('/sincronizacion/registros/', 'Listar registros de sincronización')
        
        # ADMINISTRACION MODULE
        print("\n" + "="*80)
        print("ADMINISTRACION MODULE")
        print("="*80)
        
        self.test_get('/administracion/logs-acceso/', 'Listar logs de acceso')
        self.test_get('/administracion/logs-actividad/', 'Listar logs de actividad')
        self.test_get('/administracion/backups/', 'Listar backups del sistema')
        self.test_get('/administracion/configuracion/', 'Ver configuración del sistema')
        
        # ALERTAS MODULE
        print("\n" + "="*80)
        print("ALERTAS MODULE")
        print("="*80)
        
        self.test_get('/alertas/alertas/', 'Listar alertas')
        self.test_get('/alertas/alertas/abiertas/', 'Listar alertas abiertas')
        self.test_get('/alertas/reglas/', 'Listar reglas de alertas')
        
        # NOTIFICACIONES MODULE
        print("\n" + "="*80)
        print("NOTIFICACIONES MODULE")
        print("="*80)
        
        self.test_get('/notificaciones/notificaciones/', 'Listar notificaciones')
        self.test_get('/notificaciones/notificaciones/no-leidas/', 'Listar notificaciones no leídas')
        
        # Create notificacion
        notif_data = {
            'titulo': f'Notificación Test {uuid.uuid4().hex[:4]}',
            'cuerpo': 'Esta es una notificación de prueba',
            'tipo_notificacion': 'INFORMATIVO',
            'usuario_destinatario': 2
        }
        new_notif = self.test_post('/notificaciones/notificaciones/', notif_data, 'Crear notificación')
        
        self.test_get('/notificaciones/preferencias/', 'Ver preferencias de notificaciones')
        self.test_get('/notificaciones/historial-lectura/', 'Listar historial de lectura')
        
        # SECURITY TESTS
        print("\n" + "="*80)
        print("SECURITY TESTS")
        print("="*80)
        
        # Test without token
        try:
            response = requests.get(f'{BASE_URL}/usuarios/empresas/', timeout=5)
            if response.status_code == 401:
                self.log("PASS", "/usuarios/empresas/", "GET", "Unauthorized access blocked (401)")
            else:
                self.log("FAIL", "/usuarios/empresas/", "GET", f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log("FAIL", "/usuarios/empresas/", "GET", str(e))
        
        # Test with invalid token
        try:
            headers = {'Authorization': 'Bearer invalid_token_xyz'}
            response = requests.get(f'{BASE_URL}/usuarios/empresas/', headers=headers, timeout=5)
            if response.status_code == 401:
                self.log("PASS", "/usuarios/empresas/", "GET", "Invalid token rejected (401)")
            else:
                self.log("FAIL", "/usuarios/empresas/", "GET", f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log("FAIL", "/usuarios/empresas/", "GET", str(e))
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*80)
        print("TEST REPORT")
        print("="*80)
        
        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'PASS'])
        failed = len([r for r in self.results if r['status'] == 'FAIL'])
        info = len([r for r in self.results if r['status'] == 'INFO'])
        
        print(f"\nTotal Tests: {total}")
        print(f"[OK]  Passed:    {passed} ({passed*100//total if total > 0 else 0}%)")
        print(f"[ERR] Failed:    {failed} ({failed*100//total if total > 0 else 0}%)")
        print(f"[INF] Info:      {info}")
        
        if failed > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if result['status'] == 'FAIL':
                    print(f"  - {result['method']} {result['endpoint']}: {result['message']}")
        
        print("\n" + "="*80)

if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()
