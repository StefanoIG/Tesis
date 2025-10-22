# 🌾 Sistema de Trazabilidad Agroindustrial

Backend API RESTful con Django y Django REST Framework para rastrear productos agroindustriales desde producción hasta exportación.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Módulos](#módulos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Base de Datos](#base-de-datos)

## ✨ Características

✅ **Autenticación JWT** - Tokens seguros con roles y permisos RBAC
✅ **Trazabilidad Completa** - Seguimiento de lotes desde producción hasta entrega
✅ **Offline-First** - Sincronización automática desde dispositivos móviles
✅ **Control de Calidad** - Inspecciones, análisis laboratorio y certificaciones
✅ **Logística Inteligente** - GPS tracking, alertas de desviaciones
✅ **Reportes y Análisis** - Dashboards con KPIs estratégicos
✅ **Auditoría Completa** - Logs de acceso y actividad
✅ **Sistema de Notificaciones** - Push notifications via polling (sin WebSockets)
✅ **Gestión Documental** - Subida de certificados y evidencias
✅ **API Escalable** - Diseño modular, ideal para microservicios

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                    Aplicaciones Móviles             │
│              (Android/iOS - Offline-First)          │
└────────────────────┬────────────────────────────────┘
                     │
                     │ API REST + JWT
                     │
┌────────────────────▼────────────────────────────────┐
│              Django REST Framework API               │
│  ┌──────────────────────────────────────────────┐  │
│  │  10 MÓDULOS INDEPENDIENTES Y ESCALABLES    │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    PostgreSQL    Redis      S3 AWS
```

## 🧩 Módulos

### 1. **Autenticación y Seguridad** (`autenticacion/`)
- Registro e inicio de sesión
- Tokens JWT con refresco automático
- Roles: Productor, AdminAsociación, OperadorPlanta, GerenteCalidad, etc.
- Control RBAC (Role-Based Access Control)
- Auditoría de accesos

### 2. **Trazabilidad** (`trazabilidad/`) - Core del Sistema
- Registro de lotes con código único y QR
- Seguimiento de eventos (cosecha, transporte, inspección, etc.)
- Historial completo de cambios de estado
- Validación de integridad de datos
- Ubicación GPS de eventos

### 3. **Usuarios y Roles** (`usuarios/`)
- CRUD de usuarios
- Gestión de empresas y fincas
- Asociación usuario-empresa-finca
- Permisos granulares por rol

### 4. **Procesamiento y Calidad** (`procesamiento/`)
- Registro de procesos industriales
- Inspecciones de control de calidad
- Certificaciones de cumplimiento (GlobalG.A.P, AGROCALIDAD, etc.)
- Resultados de análisis de laboratorio

### 5. **Logística** (`logistica/`)
- Gestión de vehículos y conductores
- Registro de envíos con origen/destino
- Rastreo GPS en tiempo real
- Alertas por retraso o desviación de ruta
- Monitoreo de temperatura durante transporte

### 6. **Reportes y Análisis** (`reportes/`)
- Generación de reportes (PDF, CSV, Excel)
- KPIs: producción, calidad, logística, cumplimiento
- Dashboards personalizados por rol
- Exportación de datos

### 7. **Documentos y Evidencias** (`documentos/`)
- Subida de certificados y comprobantes (S3)
- Fotos de productos en diferentes etapas
- Validación de autenticidad con hash
- Asociación a lotes y eventos

### 8. **Sincronización** (`sincronizacion/`)
- Control de sincronización por dispositivo
- Detección y resolución de conflictos
- Versiones de base de datos local
- Monitoreo de estado de sincronización

### 9. **Administración del Sistema** (`administracion/`)
- Configuración global del sistema
- Logs de acceso y actividad
- Gestión de backups
- Monitoreo del sistema

### 10. **Alertas y Notificaciones** (`alertas/`, `notificaciones/`)
- Reglas de alertas automáticas
- Sistema de notificaciones por polling
- Preferencias de notificación por usuario
- Historial de lectura de notificaciones

## 🚀 Instalación

### Requisitos Previos
- Python 3.8+
- PostgreSQL 12+
- PostGIS (extensión geoespacial)
- pip y virtualenv

### Pasos

#### 1. Clonar y preparar entorno
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tu configuración
```

#### 3. Crear base de datos
```bash
createdb trazabilidad_db
psql -d trazabilidad_db -c "CREATE EXTENSION postgis;"
```

#### 4. Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

#### 6. Ejecutar servidor
```bash
python manage.py runserver
```

## ⚙️ Configuración

### .env - Variables Importantes

```env
# Base de Datos
DB_NAME=trazabilidad_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost

# Seguridad
DJANGO_SECRET_KEY=tu_clave_secreta
DEBUG=False  # Cambiar a False en producción

# JWT
JWT_ACCESS_TOKEN_LIFETIME=3600  # 1 hora
JWT_REFRESH_TOKEN_LIFETIME=604800  # 7 días

# S3 (Documentos)
USE_S3=True
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_STORAGE_BUCKET_NAME=tu_bucket

# CORS
CORS_ALLOWED_ORIGINS=https://tuapp.com,https://app.tuapp.com
```

## 📚 Uso

### Autenticación

```bash
# Obtener token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -d "username=usuario&password=contraseña"

# Usar token en headers
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/trazabilidad/lotes/
```

### Crear un Lote

```bash
curl -X POST http://localhost:8000/api/v1/trazabilidad/lotes/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_lote": "LOTE-2025-001",
    "producto": "uuid-producto",
    "cantidad": 500,
    "unidad_medida": "kg",
    "fecha_produccion": "2025-01-15T10:00:00Z"
  }'
```

### Registrar Evento de Trazabilidad

```bash
curl -X POST http://localhost:8000/api/v1/trazabilidad/eventos/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "lote": "uuid-lote",
    "tipo_evento": 1,
    "descripcion": "Lote cosechado",
    "fecha_evento": "2025-01-15T10:30:00Z",
    "ubicacion": "POINT(-78.5 -0.5)"
  }'
```

## 🔌 API Endpoints

### Autenticación
- `POST /api/v1/auth/token/` - Obtener token
- `POST /api/v1/auth/token/refresh/` - Refrescar token
- `POST /api/v1/auth/registro/` - Registrar usuario

### Trazabilidad
- `GET/POST /api/v1/trazabilidad/lotes/` - Listar/Crear lotes
- `GET/PUT /api/v1/trazabilidad/lotes/{id}/` - Detalle/Actualizar lote
- `GET /api/v1/trazabilidad/lotes/{id}/eventos/` - Eventos del lote
- `POST /api/v1/trazabilidad/eventos/` - Crear evento

### Logística
- `GET/POST /api/v1/logistica/envios/` - Gestionar envíos
- `GET /api/v1/logistica/envios/{id}/tracking/` - Rastreo GPS
- `GET /api/v1/logistica/alertas/` - Alertas logísticas

### Reportes
- `POST /api/v1/reportes/reportes/` - Generar reporte
- `GET /api/v1/reportes/kpis/` - Índices KPI
- `GET /api/v1/reportes/dashboards/mi-dashboard/` - Mi dashboard

### Sincronización
- `POST /api/v1/sincronizacion/sincronizar/` - Ejecutar sincronización
- `GET /api/v1/sincronizacion/estados/` - Estado de dispositivos

### Notificaciones (Polling)
- `GET /api/v1/notificaciones/notificaciones/no-leidas/` - Notificaciones sin leer
- `PUT /api/v1/notificaciones/notificaciones/{id}/marcar-leida/` - Marcar como leída

## 📊 Base de Datos

### Tablas Principales

```
usuarios
├── id (UUID)
├── email (UNIQUE)
├── nombre_completo
├── password_hash
├── activo
├── ultimo_acceso
└── creado_en

lotes
├── id (UUID)
├── codigo_lote (UNIQUE)
├── producto_id
├── cantidad
├── estado (ENUM)
├── ubicacion_origen (POINT - GeoDjango)
├── fecha_produccion
└── fecha_vencimiento

eventos_trazabilidad
├── id (UUID)
├── lote_id
├── tipo_evento_id
├── usuario_id
├── ubicacion (POINT)
├── fecha_evento
└── temperatura_registrada

envios
├── id (UUID)
├── lote_id
├── vehiculo_id
├── conductor_id
├── ubicacion_origen (POINT)
├── ubicacion_destino (POINT)
├── fecha_salida
└── estado

notificaciones
├── id (UUID)
├── usuario_id
├── tipo_notificacion
├── titulo
├── cuerpo
├── fue_leida
└── creado_en
```

## 🔐 Seguridad

✅ Contraseñas hasheadas con PBKDF2
✅ Tokens JWT con expiración
✅ CORS configurado
✅ Validación de permisos en cada endpoint
✅ Logs de auditoría completos
✅ Rate limiting (configurable)
✅ HTTPS recomendado en producción
✅ CSRF protection

## 📱 Sincronización Offline-First

Los dispositivos móviles pueden:

1. **Registrar datos offline** en SQLite/Room local
2. **Sincronizar automáticamente** al restablecer conexión
3. **Resolver conflictos** con estrategia "última escritura gana"
4. **Recibir notificaciones** mediante polling cada N segundos
5. **Actualizar versiones** de esquema de BD

## 🐳 Despliegue con Docker

```bash
# Construir imagen
docker build -t trazabilidad-backend .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -e DB_HOST=postgres \
  -e DJANGO_SECRET_KEY=tu_clave \
  trazabilidad-backend
```

## 📖 Documentación API

La documentación interactiva está disponible en:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema**: http://localhost:8000/api/schema/

## 🐛 Troubleshooting

### Error: "Database does not have PostGIS extension"
```bash
psql -d trazabilidad_db -c "CREATE EXTENSION postgis;"
```

### Error: "relation ... does not exist"
```bash
python manage.py migrate
```

### Error: "CORS policy blocked"
Revisa `CORS_ALLOWED_ORIGINS` en `.env`

## 📞 Soporte

Para reportar bugs o sugerencias, abrir un issue en el repositorio.

## 📄 Licencia

Este proyecto está bajo licencia propietaria. Derechos reservados 2025.

---

**Hecho con ❤️ para la trazabilidad agroindustrial del Ecuador**
