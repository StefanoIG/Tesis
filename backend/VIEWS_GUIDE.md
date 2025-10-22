# 🔧 GUÍA PARA CREAR VIEWS

Esta guía te ayudará a crear los ViewSets y Views para los endpoints.

## Estructura General de Views

### 1. Importaciones Necesarias

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.trazabilidad.models import Lotes, EventosTrazabilidad
from apps.trazabilidad.serializers import (
    LotesSerializer, LotesListaSerializer, EventosTrazabilidadSerializer
)
from apps.autenticacion.models import Auditorias
```

### 2. Permisos Personalizados (Base)

Crear archivo `apps/autenticacion/permissions.py`:

```python
from rest_framework.permissions import BasePermission

class IsProductor(BasePermission):
    """Solo productores pueden crear lotes"""
    def has_permission(self, request, view):
        return request.user.roles.filter(rol__nombre_rol='PRODUCTOR').exists()

class IsGerenteCalidad(BasePermission):
    """Solo gerentes de calidad pueden inspeccionar"""
    def has_permission(self, request, view):
        return request.user.roles.filter(rol__nombre_rol='GERENTE_CALIDAD').exists()

class IsAdminSistema(BasePermission):
    """Solo admins del sistema"""
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.roles.filter(
            rol__nombre_rol='ADMIN_SISTEMA'
        ).exists()
```

### 3. ViewSet Básico para Lotes

Crear en `apps/trazabilidad/views.py`:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class LotesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Lotes.
    
    list - GET /lotes/
    create - POST /lotes/
    retrieve - GET /lotes/{id}/
    update - PUT /lotes/{id}/
    partial_update - PATCH /lotes/{id}/
    destroy - DELETE /lotes/{id}/
    
    Acciones personalizadas:
    - eventos - GET /lotes/{id}/eventos/
    - historial - GET /lotes/{id}/historial/
    - generar-qr - POST /lotes/{id}/generar-qr/
    """
    
    queryset = Lotes.objects.select_related('producto').prefetch_related(
        'eventos', 'cambios_estado'
    )
    serializer_class = LotesSerializer
    permission_classes = [IsAuthenticated]
    
    # Filtros y búsqueda
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields = ['estado', 'es_organico', 'producto']
    search_fields = ['codigo_lote', 'producto__nombre']
    ordering_fields = ['fecha_produccion', 'creado_en']
    ordering = ['-fecha_produccion']
    
    def get_serializer_class(self):
        """Usa serializer simplificado para listados"""
        if self.action == 'list':
            return LotesListaSerializer
        elif self.action == 'retrieve':
            return LotesConEventosSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Crear lote y generar QR"""
        lote = serializer.save()
        lote.generar_qr()
        lote.save()
        
        # Registrar en auditoría
        Auditorias.objects.create(
            usuario=self.request.user,
            accion='CREATE_LOTE',
            entidad_afectada='Lotes',
            registro_id=lote.id,
            datos_nuevos=serializer.data,
            resultado='EXITOSO'
        )
    
    def perform_update(self, serializer):
        """Actualizar lote y registrar cambios"""
        lote_anterior = Lotes.objects.get(pk=self.kwargs['pk'])
        lote = serializer.save()
        
        # Crear historial si cambió el estado
        if lote_anterior.estado != lote.estado:
            from apps.trazabilidad.models import HistorialEstadosLote
            HistorialEstadosLote.objects.create(
                lote=lote,
                estado_anterior=lote_anterior.estado,
                estado_nuevo=lote.estado,
                usuario=self.request.user,
                motivo=self.request.data.get('motivo_cambio_estado', '')
            )
        
        # Auditoría
        Auditorias.objects.create(
            usuario=self.request.user,
            accion='UPDATE_LOTE',
            entidad_afectada='Lotes',
            registro_id=lote.id,
            resultado='EXITOSO'
        )
    
    @action(detail=True, methods=['get'])
    def eventos(self, request, pk=None):
        """GET /lotes/{id}/eventos/ - Listar eventos del lote"""
        lote = self.get_object()
        eventos = lote.eventos.all()
        serializer = EventosTrazabilidadSerializer(eventos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def historial(self, request, pk=None):
        """GET /lotes/{id}/historial/ - Historial de cambios de estado"""
        lote = self.get_object()
        historial = lote.cambios_estado.all()
        serializer = HistorialEstadosLoteSerializer(historial, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generar_qr(self, request, pk=None):
        """POST /lotes/{id}/generar-qr/ - Generar código QR"""
        lote = self.get_object()
        lote.generar_qr()
        lote.save()
        return Response(
            {'mensaje': 'QR generado exitosamente'},
            status=status.HTTP_200_OK
        )
```

### 4. Router para ViewSets

Crear en `apps/trazabilidad/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.trazabilidad import views

router = DefaultRouter()
router.register(r'lotes', views.LotesViewSet, basename='lotes')
router.register(r'eventos', views.EventosTrazabilidadViewSet, basename='eventos')
router.register(r'productos', views.ProductosViewSet, basename='productos')

app_name = 'trazabilidad'

urlpatterns = [
    path('', include(router.urls)),
]
```

### 5. ViewSet para Autenticación

En `apps/autenticacion/views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    """Obtener token con información del usuario"""
    serializer_class = CustomTokenObtainPairSerializer

class RegistroView(APIView):
    """POST /registro/ - Registrar nuevo usuario"""
    permission_classes = []
    
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                {'mensaje': 'Usuario registrado exitosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """POST /logout/ - Cerrar sesión"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # En JWT no es necesario invalidar en servidor,
        # pero puede registrarse en auditoría
        Auditorias.objects.create(
            usuario=request.user,
            accion='LOGOUT',
            entidad_afectada='Autenticacion',
            resultado='EXITOSO'
        )
        return Response({'mensaje': 'Sesión cerrada'})
```

## Template Estándar de ViewSet

```python
class [Modelo]ViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar [Modelo].
    """
    
    queryset = [Modelo].objects.all()
    serializer_class = [Modelo]Serializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'creado_en']
    search_fields = ['nombre', 'codigo']
    ordering = ['-creado_en']
    
    def perform_create(self, serializer):
        serializer.save()
        # Registrar auditoría
        
    def perform_update(self, serializer):
        serializer.save()
        # Registrar auditoría
    
    def perform_destroy(self, instance):
        instance.delete()
        # Registrar auditoría
```

## Paso a Paso: Crear Views para Trazabilidad

### 1. Crear archivo `apps/trazabilidad/views.py`

```bash
touch apps/trazabilidad/views.py
```

### 2. Agregar las importaciones

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
```

### 3. Crear ViewSets

```python
class ProductosViewSet(viewsets.ModelViewSet):
    # ... código aquí
```

### 4. Actualizar URLs

Actualizar `apps/trazabilidad/urls.py` para usar router.

### 5. Actualizar Settings

Si es la primera vez usando ViewSets, asegurarse que está en INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'rest_framework',
    'apps.trazabilidad',
]
```

## Mejores Prácticas

✅ Usar `select_related` y `prefetch_related` para optimizar
✅ Validar permisos en nivel de objeto
✅ Registrar auditoría en cada operación
✅ Usar serializers diferentes para list vs retrieve
✅ Implementar búsqueda, filtrado y ordenamiento
✅ Documentar las acciones personalizadas

## Testing

```python
from django.test import TestCase
from rest_framework.test import APIClient

class LotesAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Crear usuario de prueba
        self.usuario = Usuarios.objects.create_user(...)
        self.client.force_authenticate(user=self.usuario)
    
    def test_crear_lote(self):
        response = self.client.post('/api/v1/trazabilidad/lotes/', {
            'codigo_lote': 'TEST-001',
            'producto': '...',
            'cantidad': 100
        })
        self.assertEqual(response.status_code, 201)
```

---

Usa esta guía para crear todos los ViewSets faltantes. ¡Éxito!
