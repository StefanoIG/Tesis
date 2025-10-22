# API Testing Guide - Django REST Framework

## Resumen Rápido

**Estado:** ✅ Operativo (85% de funcionalidad)
**Autenticación:** JWT Token
**URL Base:** http://localhost:8000/api/v1/

---

## 1. Autenticación

### Obtener Token JWT

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Stefano",
    "password": "Paladins#23"
  }'
```

**Respuesta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": "2",
    "email": "",
    "nombre_completo": "Stefano",
    "roles": []
  }
}
```

### Usar el Token

Todos los endpoints protegidos requieren el token en el header:

```bash
curl -H "Authorization: Bearer {ACCESS_TOKEN}" \
  http://localhost:8000/api/v1/usuarios/empresas/
```

---

## 2. Módulo de Usuarios

### Listar Empresas
```bash
GET /api/v1/usuarios/empresas/
Authorization: Bearer {TOKEN}
```

**Respuesta:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "6eb4dae7-7051-460b-bb26-f9b91e0454d6",
      "nombre": "Empresa ABC",
      "tipo_empresa": "PRODUCTOR",
      "email": "empresa@abc.com",
      "ciudad": "Bogota",
      "direccion": "Calle 1 No 1",
      "es_activa": true,
      "creado_en": "2025-10-21T22:40:47.612454-05:00"
    }
  ]
}
```

### Crear Empresa
```bash
POST /api/v1/usuarios/empresas/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "nombre": "Mi Empresa",
  "tipo_empresa": "PRODUCTOR",
  "email": "contacto@miempresa.com",
  "ciudad": "Bogota",
  "direccion": "Calle Principal 123",
  "telefono": "3001234567",
  "pais": "Colombia"
}
```

### Ver Detalle de Empresa
```bash
GET /api/v1/usuarios/empresas/{empresa_id}/
Authorization: Bearer {TOKEN}
```

### Crear Finca
```bash
POST /api/v1/usuarios/fincas/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "nombre": "Finca El Dorado",
  "codigo_finca": "FINCA001",
  "empresa": "6eb4dae7-7051-460b-bb26-f9b91e0454d6",
  "direccion": "Km 5 Vía Ubaté",
  "ciudad": "Ubaté",
  "coordenadas_latitud": 5.3833,
  "coordenadas_longitud": -73.3667,
  "tamaño_hectareas": 50.00
}
```

### Listar Fincas
```bash
GET /api/v1/usuarios/fincas/
Authorization: Bearer {TOKEN}
```

### Listar Fincas por Empresa
```bash
GET /api/v1/usuarios/empresas/{empresa_id}/fincas/
Authorization: Bearer {TOKEN}
```

---

## 3. Módulo de Trazabilidad

### Listar Lotes
```bash
GET /api/v1/trazabilidad/lotes/
Authorization: Bearer {TOKEN}
```

### Crear Lote
```bash
POST /api/v1/trazabilidad/lotes/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "codigo_lote": "LOTE001",
  "finca": "finca-uuid-here",
  "cultivo": "Tomate",
  "area_hectareas": 5.5,
  "fecha_siembra": "2025-01-15",
  "fecha_cosecha_esperada": "2025-04-15",
  "estado": "GERMINACION"
}
```

### Listar Eventos de Lote
```bash
GET /api/v1/trazabilidad/lotes/{lote_id}/eventos/
Authorization: Bearer {TOKEN}
```

### Registrar Evento
```bash
POST /api/v1/trazabilidad/lotes/{lote_id}/eventos/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "tipo_evento": "SIEMBRA",
  "descripcion": "Siembra de semillas certificadas",
  "fecha_evento": "2025-01-15T08:30:00Z",
  "responsable": "Juan Pérez"
}
```

### Listar Tipos de Eventos
```bash
GET /api/v1/trazabilidad/tipos-eventos/
Authorization: Bearer {TOKEN}
```

---

## 4. Módulo de Logística

### Listar Envios
```bash
GET /api/v1/logistica/envios/
Authorization: Bearer {TOKEN}
```

### Crear Envio
```bash
POST /api/v1/logistica/envios/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "numero_seguimiento": "ENVIO20251021001",
  "estado": "PENDIENTE",
  "fecha_salida": "2025-10-21T10:00:00Z",
  "origen": "Bogota",
  "destino": "Medellin"
}
```

### Listar Vehiculos
```bash
GET /api/v1/logistica/vehiculos/
Authorization: Bearer {TOKEN}
```

### Listar Conductores
```bash
GET /api/v1/logistica/conductores/
Authorization: Bearer {TOKEN}
```

### Tracking de Envio
```bash
GET /api/v1/logistica/envios/{envio_id}/tracking/
Authorization: Bearer {TOKEN}
```

---

## 5. Módulo de Procesamiento

### Listar Procesos
```bash
GET /api/v1/procesamiento/procesos/
Authorization: Bearer {TOKEN}
```

### Listar Inspecciones
```bash
GET /api/v1/procesamiento/inspecciones/
Authorization: Bearer {TOKEN}
```

### Listar Certificaciones
```bash
GET /api/v1/procesamiento/certificaciones/
Authorization: Bearer {TOKEN}
```

### Listar Análisis de Laboratorio
```bash
GET /api/v1/procesamiento/analisis-laboratorio/
Authorization: Bearer {TOKEN}
```

---

## 6. Módulo de Reportes

### Listar Reportes
```bash
GET /api/v1/reportes/reportes/
Authorization: Bearer {TOKEN}
```

### Generar Reporte
```bash
POST /api/v1/reportes/reportes/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "tipo_reporte": "TRAZABILIDAD",
  "fecha_inicio": "2025-01-01",
  "fecha_fin": "2025-12-31",
  "formato": "PDF"
}
```

---

## 7. Módulo de Documentos

### Listar Documentos
```bash
GET /api/v1/documentos/documentos/
Authorization: Bearer {TOKEN}
```

### Listar Fotos
```bash
GET /api/v1/documentos/fotos/
Authorization: Bearer {TOKEN}
```

---

## 8. Módulo de Sincronización

### Listar Estados de Sincronización
```bash
GET /api/v1/sincronizacion/estados/
Authorization: Bearer {TOKEN}
```

### Listar Conflictos
```bash
GET /api/v1/sincronizacion/conflictos/
Authorization: Bearer {TOKEN}
```

### Listar Registros
```bash
GET /api/v1/sincronizacion/registros/
Authorization: Bearer {TOKEN}
```

---

## 9. Módulo de Administración

### Listar Logs de Acceso
```bash
GET /api/v1/administracion/logs-acceso/
Authorization: Bearer {TOKEN}
```

### Listar Logs de Actividad
```bash
GET /api/v1/administracion/logs-actividad/
Authorization: Bearer {TOKEN}
```

### Listar Backups
```bash
GET /api/v1/administracion/backups/
Authorization: Bearer {TOKEN}
```

### Ver Configuración del Sistema
```bash
GET /api/v1/administracion/configuracion/
Authorization: Bearer {TOKEN}
```

---

## 10. Módulo de Alertas

### Listar Alertas
```bash
GET /api/v1/alertas/alertas/
Authorization: Bearer {TOKEN}
```

### Listar Alertas Abiertas
```bash
GET /api/v1/alertas/alertas/abiertas/
Authorization: Bearer {TOKEN}
```

### Listar Reglas
```bash
GET /api/v1/alertas/reglas/
Authorization: Bearer {TOKEN}
```

### Resolver Alerta
```bash
POST /api/v1/alertas/alertas/{alerta_id}/resolver/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "comentario": "Problema resuelto",
  "fecha_resolucion": "2025-10-21T15:30:00Z"
}
```

---

## 11. Módulo de Notificaciones

### Listar Notificaciones
```bash
GET /api/v1/notificaciones/notificaciones/
Authorization: Bearer {TOKEN}
```

### Listar Notificaciones No Leídas
```bash
GET /api/v1/notificaciones/notificaciones/no-leidas/
Authorization: Bearer {TOKEN}
```

### Crear Notificación
```bash
POST /api/v1/notificaciones/notificaciones/
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "titulo": "Nueva Alerta",
  "cuerpo": "Se ha detectado un problema en la Finca El Dorado",
  "tipo_notificacion": "ALERTA",
  "usuario": 2
}
```

### Marcar como Leída
```bash
POST /api/v1/notificaciones/notificaciones/{notificacion_id}/marcar-leida/
Authorization: Bearer {TOKEN}
```

### Marcar Todas como Leídas
```bash
POST /api/v1/notificaciones/notificaciones/marcar-todas-leidas/
Authorization: Bearer {TOKEN}
```

---

## 12. Códigos de Estado HTTP

| Código | Significado |
|--------|------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 204 | No Content - Solicitud exitosa sin contenido |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o expirado |
| 403 | Forbidden - Acceso denegado |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

---

## 13. Documentación Interactiva

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **Schema OpenAPI:** http://localhost:8000/api/schema/

---

## 14. Pruebas Automatizadas

### Ejecutar suite de pruebas
```bash
cd backend
python test_api2.py
```

### Ejecutar test básico
```bash
cd backend
python test_api.py
```

---

## 15. Tipos de Empresa Válidos

```
PRODUCTOR - Productor Agrícola
ACOPIO - Centro de Acopio
TRANSFORMACION - Empresa de Transformación
EXPORTADOR - Empresa Exportadora
DISTRIBUIDOR - Distribuidor
ASOCIACION - Asociación Productiva
```

---

## 16. Estados de Lote Válidos

```
GERMINACION - Germinación
CRECIMIENTO - Crecimiento
MADUREZ - Madurez
COSECHA - Cosecha
POSTCOSECHA - Postcosecha
```

---

## 17. Tipos de Notificación

```
INFORMATIVO - Información general
ALERTA - Alerta importante
CRITICA - Alerta crítica
```

---

## Errores Comunes

### "Token inválido"
- Asegúrate de incluir el token en el header
- Verifica que el token no haya expirado
- Usa `Authorization: Bearer {TOKEN}` (nota el espacio)

### "Campo requerido"
- Revisa que todos los campos obligatorios estén presentes
- Consulta Swagger para ver los campos requeridos de cada endpoint

### "401 Unauthorized"
- Necesitas autenticarte primero
- Obtén un token usando `/auth/token/`
- Incluye el token en todos los requests a endpoints protegidos

---

*Última actualización: 2025-10-21*
