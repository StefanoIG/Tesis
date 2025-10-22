Project TrazabilidadAgroindustrial {
  database_type: "PostgreSQL"
  note: "Base de datos modular para trazabilidad agroindustrial en Manta - Diseño basado en GS1 Global Traceability Standard"
}

// ========================================
// MÓDULO: GESTIÓN DE USUARIOS Y ROLES (RBAC)
// ========================================

Table Usuarios {
  id uuid [pk, default: `gen_random_uuid()`]
  nombre_completo varchar(255) [not null]
  email varchar(255) [unique, not null]
  password_hash varchar(255) [not null]
  telefono varchar(20)
  activo boolean [default: true]
  ultimo_acceso timestamptz
  creado_en timestamptz [default: `now()`, not null]
  actualizado_en timestamptz [default: `now()`, not null]

  indexes {
    email [unique]
  }

  note: "Almacena información de todos los actores del sistema"
}

Table Roles {
  id serial [pk]
  nombre_rol varchar(50) [unique, not null]
  descripcion text

  note: "Roles: Productor, AdminAsociacion, OperadorPlanta, GerenteCalidad, GerenteLogistica, AdminSistema, Auditor"
}

Table UsuariosRoles {
  usuario_id uuid [pk, ref: > Usuarios.id]
  rol_id int [pk, ref: > Roles.id]
  asignado_en timestamptz [default: `now()`]

  note: "Tabla de unión para implementar RBAC (Control de Acceso Basado en Roles)"
}

// ========================================
// MÓDULO: PRODUCTORES Y ORGANIZACIONES
// ========================================

Table Productores {
  id uuid [pk, default: `gen_random_uuid()`]
  usuario_id uuid [ref: > Usuarios.id]
  tipo_productor varchar(50) [not null]
  identificacion varchar(20) [unique, not null]
  razon_social varchar(255)
  direccion text
  geolocalizacion geography(point, 4326)
  superficie_ha decimal(10,2)
  capacidad_produccion_mensual decimal(10,2)
  certificaciones_vigentes text[]
  creado_en timestamptz [default: `now()`]
  actualizado_en timestamptz [default: `now()`]

  indexes {
    (tipo_productor)
    (geolocalizacion) [type: gist]
  }

  note: "Tipos: Agricultor, Ganadero, Pescador, Acuicultor. Incluye geolocalización para funcionalidad offline-first"
}

Table Asociaciones {
  id uuid [pk, default: `gen_random_uuid()`]
  nombre varchar(255) [not null]
  tipo varchar(50)
  representante_legal varchar(255)
  identificacion_fiscal varchar(20) [unique]
  direccion text
  telefono varchar(20)
  email varchar(100)
  creado_en timestamptz [default: `now()`]

  note: "Cooperativas y asociaciones que agrupan a productores"
}

Table ProductoresAsociaciones {
  productor_id uuid [pk, ref: > Productores.id]
  asociacion_id uuid [pk, ref: > Asociaciones.id]
  fecha_ingreso date [not null]
  fecha_salida date
  activo boolean [default: true]
}

// ========================================
// MÓDULO: CATÁLOGO DE PRODUCTOS
// ========================================

Table Productos {
  id uuid [pk, default: `gen_random_uuid()`]
  nombre varchar(100) [not null]
  nombre_cientifico varchar(150)
  categoria varchar(50) [not null]
  subcategoria varchar(50)
  variedad varchar(100)
  descripcion text
  codigo_gs1 varchar(50) [unique]
  unidad_medida_base varchar(20) [not null]
  requiere_cadena_frio boolean [default: false]
  temperatura_optima_min decimal(5,2)
  temperatura_optima_max decimal(5,2)
  dias_vida_util int
  normativas_aplicables text[]
  creado_en timestamptz [default: `now()`]
  actualizado_en timestamptz [default: `now()`]

  indexes {
    (categoria)
    (codigo_gs1) [unique]
  }

  note: "Categorías: Cacao, Plátano, Atún, Camarón, Ganado, Maíz. Incluye parámetros de calidad e inocuidad"
}

// ========================================
// MÓDULO CENTRAL: LOTES Y TRAZABILIDAD
// ========================================

Table Lotes {
  id uuid [pk, default: `gen_random_uuid()`]
  codigo_lote varchar(50) [unique, not null]
  producto_id uuid [ref: > Productos.id, not null]
  productor_id uuid [ref: > Productores.id]
  asociacion_id uuid [ref: > Asociaciones.id]
  cantidad_inicial decimal(10,2) [not null]
  cantidad_actual decimal(10,2) [not null]
  unidad_medida varchar(20) [not null]
  fecha_creacion date [not null]
  estado varchar(30) [not null, default: 'En_Origen']
  codigo_qr text
  metadata_adicional jsonb
  creado_en timestamptz [default: `now()`, not null]
  actualizado_en timestamptz [default: `now()`, not null]

  indexes {
    (codigo_lote) [unique]
    (estado)
    (producto_id, fecha_creacion)
    (metadata_adicional) [type: gin]
  }

  note: "Estados: En_Origen, En_Transito, En_Acopio, En_Procesamiento, En_Almacen, Exportado, Distribuido, Retirado. Código QR generado automáticamente"
}

// ========================================
// MÓDULO: EVENTOS DE TRAZABILIDAD (GS1)
// ========================================

Table EventosTrazabilidad {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_id uuid [ref: > Lotes.id, not null]
  tipo_evento varchar(50) [not null]
  subtipo_evento varchar(50)
  usuario_id uuid [ref: > Usuarios.id, not null]
  ubicacion_id uuid [ref: > Ubicaciones.id]
  geolocalizacion geography(point, 4326)
  fecha_evento timestamptz [not null]
  cantidad_afectada decimal(10,2)
  unidad_medida varchar(20)
  descripcion text
  temperatura decimal(5,2)
  humedad decimal(5,2)
  datos_adicionales jsonb
  documentos_adjuntos text[]
  evento_padre_id uuid [ref: > EventosTrazabilidad.id]
  sincronizado boolean [default: false]
  creado_en timestamptz [default: `now()`, not null]

  indexes {
    (lote_id, fecha_evento)
    (tipo_evento)
    (usuario_id)
    (ubicacion_id)
    (fecha_evento)
    (geolocalizacion) [type: gist]
    (datos_adicionales) [type: gin]
  }

  note: "Tipos: COSECHA, RECEPCION, ACOPIO, FERMENTACION, SECADO, CLASIFICACION, ALMACENAMIENTO, TRANSPORTE, PROCESAMIENTO, ENVASADO, CONTROL_CALIDAD, EMBARQUE, INSPECCION, INCIDENTE. Basado en GS1 'Who, What, When, Where, Why'"
}

// ========================================
// MÓDULO: UBICACIONES Y LOGÍSTICA
// ========================================

Table Ubicaciones {
  id uuid [pk, default: `gen_random_uuid()`]
  nombre varchar(255) [not null]
  tipo varchar(50) [not null]
  codigo_identificacion varchar(50) [unique]
  direccion text
  geolocalizacion geography(point, 4326)
  provincia varchar(50)
  canton varchar(50)
  parroquia varchar(50)
  contacto_nombre varchar(100)
  contacto_telefono varchar(20)
  contacto_email varchar(100)
  capacidad_almacenamiento decimal(10,2)
  tiene_cadena_frio boolean [default: false]
  certificaciones text[]
  activo boolean [default: true]
  creado_en timestamptz [default: `now()`]

  indexes {
    (tipo)
    (geolocalizacion) [type: gist]
    (provincia, canton)
  }

  note: "Tipos: Finca, Centro_Acopio, Planta_Procesamiento, Almacen, Puerto, Bodega_Refrigerada, Punto_Inspeccion"
}

Table Transportes {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_id uuid [ref: > Lotes.id, not null]
  tipo_transporte varchar(50)
  vehiculo_placa varchar(20)
  conductor_nombre varchar(100)
  conductor_identificacion varchar(20)
  origen_id uuid [ref: > Ubicaciones.id, not null]
  destino_id uuid [ref: > Ubicaciones.id, not null]
  fecha_salida timestamptz [not null]
  fecha_llegada_estimada timestamptz
  fecha_llegada_real timestamptz
  temperatura_minima decimal(5,2)
  temperatura_maxima decimal(5,2)
  requiere_refrigeracion boolean [default: false]
  estado varchar(30) [default: 'Planificado']
  observaciones text
  ruta_gps jsonb
  creado_en timestamptz [default: `now()`]

  indexes {
    (lote_id)
    (estado)
    (fecha_salida, fecha_llegada_estimada)
  }

  note: "Estados: Planificado, En_Transito, Completado, Cancelado, Incidente. Incluye tracking GPS"
}

Table LecturasTemperatura {
  id uuid [pk, default: `gen_random_uuid()`]
  transporte_id uuid [ref: > Transportes.id]
  lote_id uuid [ref: > Lotes.id]
  ubicacion_id uuid [ref: > Ubicaciones.id]
  temperatura decimal(5,2) [not null]
  humedad decimal(5,2)
  geolocalizacion geography(point, 4326)
  fecha_lectura timestamptz [not null]
  dispositivo_sensor varchar(100)
  alerta_generada boolean [default: false]

  indexes {
    (transporte_id, fecha_lectura)
    (lote_id, fecha_lectura)
    (alerta_generada)
  }

  note: "Monitoreo de temperatura para cadena de frío"
}

// ========================================
// MÓDULO: CONTROL DE CALIDAD E INOCUIDAD
// ========================================

Table ParametrosCalidad {
  id uuid [pk, default: `gen_random_uuid()`]
  producto_id uuid [ref: > Productos.id, not null]
  nombre_parametro varchar(100) [not null]
  tipo_parametro varchar(50)
  unidad_medida varchar(20)
  valor_minimo decimal(10,4)
  valor_maximo decimal(10,4)
  valor_objetivo decimal(10,4)
  metodo_analisis varchar(255)
  normativa_referencia varchar(255)
  es_critico boolean [default: false]
  activo boolean [default: true]

  indexes {
    (producto_id)
    (es_critico)
  }

  note: "Parámetros: Humedad, Fermentación, Madurez, pH, Micotoxinas, Patógenos, Residuos, etc."
}

Table AnalisisCalidad {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_id uuid [ref: > Lotes.id, not null]
  parametro_id uuid [ref: > ParametrosCalidad.id, not null]
  evaluador_id uuid [ref: > Usuarios.id, not null]
  laboratorio varchar(255)
  valor_medido decimal(10,4)
  unidad_medida varchar(20)
  resultado varchar(20) [not null]
  conformidad boolean [not null]
  fecha_analisis timestamptz [not null]
  fecha_resultado timestamptz
  metodo_utilizado varchar(255)
  observaciones text
  certificado_url text
  evidencia_fotografica text[]

  indexes {
    (lote_id, fecha_analisis)
    (resultado)
    (conformidad)
  }

  note: "Resultados: Aprobado, Aprobado_Condicional, Rechazado, Pendiente. Vinculado a eventos de trazabilidad"
}

Table NoConformidades {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_id uuid [ref: > Lotes.id, not null]
  analisis_id uuid [ref: > AnalisisCalidad.id]
  tipo_no_conformidad varchar(50) [not null]
  gravedad varchar(20) [not null]
  descripcion text [not null]
  detectado_por_id uuid [ref: > Usuarios.id, not null]
  fecha_deteccion timestamptz [not null]
  estado varchar(30) [default: 'Abierta']
  accion_correctiva text
  responsable_correccion_id uuid [ref: > Usuarios.id]
  fecha_correccion timestamptz
  verificado_por_id uuid [ref: > Usuarios.id]
  fecha_verificacion timestamptz

  indexes {
    (lote_id)
    (estado)
    (gravedad)
  }

  note: "Estados: Abierta, En_Correccion, Corregida, Verificada, Cerrada. Gravedad: Baja, Media, Alta, Crítica"
}

// ========================================
// MÓDULO: PROCESAMIENTO Y TRANSFORMACIÓN
// ========================================

Table Procesos {
  id uuid [pk, default: `gen_random_uuid()`]
  nombre_proceso varchar(100) [not null]
  tipo_proceso varchar(50) [not null]
  producto_entrada_id uuid [ref: > Productos.id]
  producto_salida_id uuid [ref: > Productos.id]
  descripcion text
  duracion_estimada_horas int
  temperatura_proceso decimal(5,2)
  requiere_supervision boolean [default: true]

  note: "Tipos: Fermentación, Secado, Limpieza, Clasificación, Fileteado, Congelado, Enlatado, Empaque, etc."
}

Table ProcesamientoLotes {
  id uuid [pk, default: `gen_random_uuid()`]
  proceso_id uuid [ref: > Procesos.id, not null]
  lote_entrada_id uuid [ref: > Lotes.id, not null]
  lote_salida_id uuid [ref: > Lotes.id]
  ubicacion_id uuid [ref: > Ubicaciones.id, not null]
  responsable_id uuid [ref: > Usuarios.id, not null]
  fecha_inicio timestamptz [not null]
  fecha_fin timestamptz
  cantidad_entrada decimal(10,2) [not null]
  cantidad_salida decimal(10,2)
  porcentaje_rendimiento decimal(5,2)
  estado varchar(30) [default: 'En_Proceso']
  parametros_proceso jsonb
  observaciones text

  indexes {
    (lote_entrada_id)
    (lote_salida_id)
    (estado)
    (fecha_inicio)
  }

  note: "Estados: Planificado, En_Proceso, Completado, Suspendido, Fallido. Permite trazabilidad interna"
}

Table MezclasLotes {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_destino_id uuid [ref: > Lotes.id, not null]
  lote_origen_id uuid [ref: > Lotes.id, not null]
  cantidad_mezclada decimal(10,2) [not null]
  proporcion_porcentaje decimal(5,2)
  fecha_mezcla timestamptz [not null]
  responsable_id uuid [ref: > Usuarios.id, not null]
  motivo text

  indexes {
    (lote_destino_id)
    (lote_origen_id)
  }

  note: "Gestiona divisiones y mezclas de lotes para mantener trazabilidad interna"
}

// ========================================
// MÓDULO: CERTIFICACIONES Y CUMPLIMIENTO
// ========================================

Table Certificaciones {
  id uuid [pk, default: `gen_random_uuid()`]
  nombre varchar(100) [not null, unique]
  tipo_certificacion varchar(50)
  entidad_emisora varchar(100) [not null]
  alcance varchar(50)
  descripcion text
  url_informacion text
  logo_url text
  vigencia_anios int
  activo boolean [default: true]

  note: "Ejemplos: GlobalG.A.P., FSMA, BPA, Orgánico, Fair Trade, Rainforest Alliance, ISO 22000"
}

Table CertificacionesProductores {
  id uuid [pk, default: `gen_random_uuid()`]
  certificacion_id uuid [ref: > Certificaciones.id, not null]
  productor_id uuid [ref: > Productores.id]
  asociacion_id uuid [ref: > Asociaciones.id]
  numero_certificado varchar(100) [unique, not null]
  fecha_emision date [not null]
  fecha_expiracion date [not null]
  estado varchar(30) [default: 'Vigente']
  archivo_certificado text
  alcance_productos text[]
  observaciones text

  indexes {
    (estado, fecha_expiracion)
    (numero_certificado) [unique]
  }

  note: "Estados: Vigente, Por_Renovar, Vencida, Suspendida, Revocada"
}

Table CertificacionesLotes {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_id uuid [ref: > Lotes.id, not null]
  certificacion_productor_id uuid [ref: > CertificacionesProductores.id, not null]
  verificado_por_id uuid [ref: > Usuarios.id]
  fecha_verificacion timestamptz
  archivo_evidencia text

  indexes {
    (lote_id)
  }

  note: "Vincula lotes específicos con certificaciones del productor"
}

Table RequisitosCumplimiento {
  id uuid [pk, default: `gen_random_uuid()`]
  certificacion_id uuid [ref: > Certificaciones.id]
  normativa varchar(100)
  pais_destino varchar(50)
  requisito text [not null]
  tipo_requisito varchar(50)
  es_obligatorio boolean [default: true]
  documentacion_requerida text[]
  frecuencia_verificacion varchar(50)

  indexes {
    (normativa)
    (pais_destino)
  }

  note: "Requisitos de FDA, UE, AGROCALIDAD, etc. Tipos: Documentación, Análisis, Inspección, Registro"
}

Table CumplimientoNormativo {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_id uuid [ref: > Lotes.id, not null]
  requisito_id uuid [ref: > RequisitosCumplimiento.id, not null]
  cumplido boolean [not null]
  fecha_verificacion timestamptz [not null]
  verificado_por_id uuid [ref: > Usuarios.id, not null]
  evidencia_url text
  observaciones text

  indexes {
    (lote_id)
    (cumplido)
  }

  note: "Registro de cumplimiento de requisitos específicos por lote"
}

// ========================================
// MÓDULO: ALERTAS E INCIDENTES
// ========================================

Table TiposAlerta {
  id serial [pk]
  nombre varchar(50) [unique, not null]
  categoria varchar(30) [not null]
  nivel_gravedad varchar(20) [not null]
  descripcion text
  accion_automatica text

  note: "Categorías: Calidad, Temperatura, Seguridad, Documentacion, Vencimiento. Niveles: Informativa, Baja, Media, Alta, Crítica"
}

Table Alertas {
  id uuid [pk, default: `gen_random_uuid()`]
  tipo_alerta_id int [ref: > TiposAlerta.id, not null]
  lote_id uuid [ref: > Lotes.id]
  transporte_id uuid [ref: > Transportes.id]
  lectura_temperatura_id uuid [ref: > LecturasTemperatura.id]
  analisis_id uuid [ref: > AnalisisCalidad.id]
  mensaje text [not null]
  nivel varchar(20) [not null]
  fecha_generacion timestamptz [default: `now()`, not null]
  estado varchar(30) [default: 'Activa']
  atendida_por_id uuid [ref: > Usuarios.id]
  fecha_atencion timestamptz
  accion_tomada text

  indexes {
    (estado, nivel)
    (lote_id)
    (fecha_generacion)
  }

  note: "Estados: Activa, En_Atencion, Resuelta, Falsa_Alarma, Escalada"
}

Table Incidentes {
  id uuid [pk, default: `gen_random_uuid()`]
  lote_id uuid [ref: > Lotes.id]
  tipo_incidente varchar(50) [not null]
  gravedad varchar(20) [not null]
  descripcion text [not null]
  ubicacion_id uuid [ref: > Ubicaciones.id]
  geolocalizacion geography(point, 4326)
  reportado_por_id uuid [ref: > Usuarios.id, not null]
  fecha_incidente timestamptz [not null]
  fecha_reporte timestamptz [default: `now()`]
  estado varchar(30) [default: 'Reportado']
  impacto_estimado text
  acciones_inmediatas text
  responsable_gestion_id uuid [ref: > Usuarios.id]
  fecha_resolucion timestamptz
  resolucion_final text
  evidencia_fotografica text[]
  documentos_adjuntos text[]

  indexes {
    (estado)
    (gravedad)
    (fecha_incidente)
    (lote_id)
  }

  note: "Tipos: Contaminacion, Accidente, Robo, Deterioro, Incumplimiento_Temperatura, Retraso. Estados: Reportado, En_Investigacion, En_Correccion, Resuelto, Cerrado"
}

Table RetiradaProductos {
  id uuid [pk, default: `gen_random_uuid()`]
  incidente_id uuid [ref: > Incidentes.id]
  tipo_retirada varchar(30) [not null]
  alcance varchar(20) [not null]
  razon text [not null]
  fecha_decision timestamptz [not null]
  autorizado_por_id uuid [ref: > Usuarios.id, not null]
  estado varchar(30) [default: 'Planificada']
  notificacion_clientes boolean [default: false]
  notificacion_autoridades boolean [default: false]
  fecha_inicio_retirada timestamptz
  fecha_finalizacion timestamptz
  cantidad_afectada decimal(10,2)
  cantidad_recuperada decimal(10,2)
  costo_estimado decimal(12,2)
  informe_final text

  indexes {
    (estado)
    (fecha_decision)
  }

  note: "Tipos: Voluntaria, Obligatoria. Alcance: Lote_Especifico, Producto, Productor, Regional, Nacional. Estados: Planificada, En_Proceso, Completada, Suspendida"
}

Table LotesAfectadosRetirada {
  retirada_id uuid [pk, ref: > RetiradaProductos.id]
  lote_id uuid [pk, ref: > Lotes.id]
  cantidad_retirada decimal(10,2)
  estado_recuperacion varchar(30)
  fecha_notificacion timestamptz
  fecha_recuperacion timestamptz

  note: "Trazabilidad hacia adelante para retiradas selectivas"
}

// ========================================
// MÓDULO: GESTIÓN DOCUMENTAL
// ========================================

Table TiposDocumento {
  id serial [pk]
  nombre varchar(50) [unique, not null]
  categoria varchar(30)
  descripcion text
  obligatorio boolean [default: false]
  formato_aceptado text[]

  note: "Ejemplos: Certificado_Analisis, Guia_Remision, Permiso_Exportacion, Factura, BPA, BPM, Foto_Producto"
}

Table Documentos {
  id uuid [pk, default: `gen_random_uuid()`]
  tipo_documento_id int [ref: > TiposDocumento.id, not null]
  nombre_archivo varchar(255) [not null]
  descripcion text
  url_almacenamiento text [not null]
  tamanio_bytes bigint
  formato varchar(10)
  hash_integridad varchar(64)
  subido_por_id uuid [ref: > Usuarios.id, not null]
  fecha_subida timestamptz [default: `now()`, not null]
  fecha_vigencia date

  indexes {
    (tipo_documento_id)
    (fecha_subida)
  }

  note: "Almacena documentos en S3 u otro servicio de almacenamiento de objetos"
}

Table DocumentosLotes {
  documento_id uuid [pk, ref: > Documentos.id]
  lote_id uuid [pk, ref: > Lotes.id]
  relevancia varchar(20) [default: 'Media']

  note: "Vincula documentos con lotes específicos"
}

Table DocumentosEventos {
  documento_id uuid [pk, ref: > Documentos.id]
  evento_id uuid [pk, ref: > EventosTrazabilidad.id]

  note: "Vincula documentos con eventos específicos de trazabilidad"
}

// ========================================
// MÓDULO: SINCRONIZACIÓN OFFLINE-FIRST
// ========================================

Table ColaSincronizacion {
  id uuid [pk, default: `gen_random_uuid()`]
  usuario_id uuid [ref: > Usuarios.id, not null]
  dispositivo_id varchar(100)
  tabla_afectada varchar(50) [not null]
  registro_id uuid [not null]
  operacion varchar(10) [not null]
  datos_json jsonb [not null]
  timestamp_cliente timestamptz [not null]
  timestamp_servidor timestamptz [default: `now()`]
  sincronizado boolean [default: false]
  intentos_sincronizacion int [default: 0]
  ultimo_intento timestamptz
  error_sincronizacion text
  resuelto boolean [default: false]

  indexes {
    (sincronizado)
    (usuario_id, tabla_afectada)
    (timestamp_cliente)
  }

  note: "Operaciones: INSERT, UPDATE, DELETE. Gestiona conflictos con estrategia Last-Write-Wins"
}

Table DispositivosMoviles {
  id uuid [pk, default: `gen_random_uuid()`]
  usuario_id uuid [ref: > Usuarios.id, not null]
  identificador_dispositivo varchar(100) [unique, not null]
  modelo varchar(100)
  sistema_operativo varchar(50)
  version_app varchar(20)
  ultimo_acceso timestamptz
  estado varchar(20) [default: 'Activo']
  token_push text

  indexes {
    (usuario_id)
    (identificador_dispositivo) [unique]
  }

  note: "Estados: Activo, Inactivo, Bloqueado, Eliminado"
}

// ========================================
// MÓDULO: REPORTES Y ANALYTICS
// ========================================

Table PlantillasReporte {
  id uuid [pk, default: `gen_random_uuid()`]
  nombre varchar(100) [not null]
  tipo_reporte varchar(50) [not null]
  descripcion text
  parametros_requeridos jsonb
  query_sql text
  formato_salida varchar(20) [not null]
  roles_autorizados int[] [ref: > Roles.id]
  activo boolean [default: true]

  note: "Tipos: Trazabilidad_Lote, Resumen_Calidad, Cumplimiento_Normativo, Productividad, KPIs. Formatos: PDF, Excel, CSV, JSON"
}

Table ReportesGenerados {
  id uuid [pk, default: `gen_random_uuid()`]
  plantilla_id uuid [ref: > PlantillasReporte.id, not null]
  generado_por_id uuid [ref: > Usuarios.id, not null]
  fecha_generacion timestamptz [default: `now()`, not null]
  parametros_utilizados jsonb
  url_archivo text
  formato varchar(20)
  tamanio_bytes bigint

  indexes {
    (generado_por_id, fecha_generacion)
    (plantilla_id)
  }
}

// ========================================
// MÓDULO: AUDITORÍA Y TRAZABILIDAD DEL SISTEMA
// ========================================

Table Auditorias {
  id uuid [pk, default: `gen_random_uuid()`]
  usuario_id uuid [ref: > Usuarios.id]
  accion varchar(100) [not null]
  entidad_afectada varchar(50) [not null]
  registro_id uuid
  datos_anteriores jsonb
  datos_nuevos jsonb
  ip_origen inet
  user_agent text
  timestamp timestamptz [default: `now()`, not null]
  resultado varchar(20) [default: 'Exitoso']
  mensaje_error text

  indexes {
    (usuario_id, timestamp)
    (entidad_afectada, registro_id)
    (timestamp)
  }

  note: "Log completo de todas las operaciones críticas para auditoría y cumplimiento normativo"
}

// ========================================
// MÓDULO: NOTIFICACIONES
// ========================================

Table Notificaciones {
  id uuid [pk, default: `gen_random_uuid()`]
  usuario_id uuid [ref: > Usuarios.id, not null]
  tipo_notificacion varchar(50) [not null]
  titulo varchar(255) [not null]
  mensaje text [not null]
  leida boolean [default: false]
  fecha_lectura timestamptz
  url_destino text
  entidad_relacionada varchar(50)
  entidad_id uuid
  creado_en timestamptz [default: `now()`, not null]
  
  indexes {
    (usuario_id, leida)
    (creado_en)
  }
  
  note: "Gestiona notificaciones in-app y push para los usuarios. Tipos: Alerta, Tarea_Asignada, Mencion, Sistema, Cumplimiento"
}