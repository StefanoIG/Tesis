from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Avg, Max, Min, Count, Q
from datetime import timedelta

from .models import (
    DispositivosSensores, LecturasSensores,
    ConfiguracionesAlertasSensor, RegistrosMantenimientoSensor
)
from .serializers import (
    DispositivosSensoresSerializer, LecturasSensoresSerializer,
    LecturaSensorCreateSerializer,
    ConfiguracionesAlertasSensorSerializer,
    RegistrosMantenimientoSensorSerializer
)


class DispositivosSensoresViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de dispositivos sensores.
    """
    queryset = DispositivosSensores.objects.select_related(
        'empresa', 'finca', 'ubicacion'
    ).all()
    serializer_class = DispositivosSensoresSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'finca', 'ubicacion', 'tipo_dispositivo', 'estado']
    search_fields = ['codigo_dispositivo', 'nombre', 'numero_serie']
    ordering_fields = ['nombre', 'fecha_instalacion']
    ordering = ['empresa', 'nombre']

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtiene dispositivos activos."""
        dispositivos = self.queryset.filter(estado='ACTIVO')
        serializer = self.get_serializer(dispositivos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def requieren_mantenimiento(self, request):
        """Obtiene dispositivos que requieren mantenimiento próximo."""
        fecha_limite = timezone.now().date() + timedelta(days=30)
        dispositivos = self.queryset.filter(
            Q(fecha_proximo_mantenimiento__lte=fecha_limite) |
            Q(fecha_proximo_mantenimiento__isnull=True, estado='ACTIVO')
        )
        serializer = self.get_serializer(dispositivos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtiene estadísticas de un dispositivo."""
        dispositivo = self.get_object()
        
        # Últimas 24 horas
        hace_24h = timezone.now() - timedelta(hours=24)
        lecturas_24h = dispositivo.lecturas.filter(fecha_lectura__gte=hace_24h)
        
        stats = {
            'total_lecturas': dispositivo.lecturas.count(),
            'lecturas_ultimas_24h': lecturas_24h.count(),
            'ultima_lectura': dispositivo.ultima_lectura_fecha,
            'alertas_generadas': dispositivo.lecturas.filter(alerta_generada=True).count(),
        }
        
        # Estadísticas por tipo de medición
        tipos_medicion = dispositivo.lecturas.values('tipo_medicion').distinct()
        for tipo in tipos_medicion:
            tipo_nombre = tipo['tipo_medicion']
            lecturas_tipo = dispositivo.lecturas.filter(tipo_medicion=tipo_nombre)
            stats[f'{tipo_nombre}_promedio'] = lecturas_tipo.aggregate(Avg('valor'))['valor__avg']
            stats[f'{tipo_nombre}_min'] = lecturas_tipo.aggregate(Min('valor'))['valor__min']
            stats[f'{tipo_nombre}_max'] = lecturas_tipo.aggregate(Max('valor'))['valor__max']
        
        return Response(stats)


class LecturasSensoresViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de lecturas de sensores.
    """
    queryset = LecturasSensores.objects.select_related(
        'dispositivo', 'lote', 'transporte', 'ubicacion', 'registrado_por'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        'dispositivo', 'lote', 'transporte', 'ubicacion',
        'tipo_medicion', 'fuente', 'alerta_generada'
    ]
    ordering_fields = ['fecha_lectura', 'valor']
    ordering = ['-fecha_lectura']

    def get_serializer_class(self):
        if self.action == 'create':
            return LecturaSensorCreateSerializer
        return LecturasSensoresSerializer

    @action(detail=False, methods=['post'])
    def registrar_manual(self, request):
        """Registra una lectura manual."""
        serializer = LecturaSensorCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            lectura = serializer.save()
            
            # Evaluar alertas si hay dispositivo asociado
            if lectura.dispositivo:
                self._evaluar_alertas(lectura)
            
            return Response(
                LecturasSensoresSerializer(lectura).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def por_lote(self, request):
        """Obtiene lecturas de un lote específico."""
        lote_id = request.query_params.get('lote_id')
        if not lote_id:
            return Response(
                {'error': 'Se requiere parámetro lote_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lecturas = self.queryset.filter(lote_id=lote_id)
        serializer = self.get_serializer(lecturas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def alertas(self, request):
        """Obtiene lecturas que generaron alertas."""
        lecturas = self.queryset.filter(alerta_generada=True)
        
        # Filtros opcionales
        dias = request.query_params.get('dias')
        if dias:
            fecha_desde = timezone.now() - timedelta(days=int(dias))
            lecturas = lecturas.filter(fecha_lectura__gte=fecha_desde)
        
        serializer = self.get_serializer(lecturas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen_por_dispositivo(self, request):
        """Obtiene resumen de lecturas por dispositivo."""
        dispositivo_id = request.query_params.get('dispositivo_id')
        if not dispositivo_id:
            return Response(
                {'error': 'Se requiere parámetro dispositivo_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lecturas = self.queryset.filter(dispositivo_id=dispositivo_id)
        
        # Agrupar por tipo de medición
        resumen = {}
        for tipo in lecturas.values('tipo_medicion').distinct():
            tipo_nombre = tipo['tipo_medicion']
            lecturas_tipo = lecturas.filter(tipo_medicion=tipo_nombre)
            
            resumen[tipo_nombre] = {
                'total_lecturas': lecturas_tipo.count(),
                'promedio': lecturas_tipo.aggregate(Avg('valor'))['valor__avg'],
                'minimo': lecturas_tipo.aggregate(Min('valor'))['valor__min'],
                'maximo': lecturas_tipo.aggregate(Max('valor'))['valor__max'],
                'ultima_lectura': lecturas_tipo.latest('fecha_lectura').valor,
                'alertas': lecturas_tipo.filter(alerta_generada=True).count()
            }
        
        return Response(resumen)

    def _evaluar_alertas(self, lectura):
        """Evalúa si una lectura debe generar alertas."""
        # Buscar configuraciones activas
        configuraciones = ConfiguracionesAlertasSensor.objects.filter(
            Q(dispositivo=lectura.dispositivo) | Q(empresa=lectura.dispositivo.empresa),
            tipo_medicion=lectura.tipo_medicion,
            es_activa=True
        )
        
        for config in configuraciones:
            if config.evaluar_lectura(lectura.valor):
                lectura.alerta_generada = True
                lectura.fuera_de_rango = True
                lectura.save()
                
                # TODO: Crear notificación/alerta en el sistema
                # TODO: Enviar notificaciones push si está configurado
                break


class ConfiguracionesAlertasSensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para configuraciones de alertas de sensores.
    """
    queryset = ConfiguracionesAlertasSensor.objects.select_related(
        'dispositivo', 'empresa'
    ).prefetch_related('usuarios_notificar').all()
    serializer_class = ConfiguracionesAlertasSensorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['dispositivo', 'empresa', 'tipo_medicion', 'nivel_alerta', 'es_activa']
    search_fields = ['nombre', 'descripcion']

    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activa una configuración de alerta."""
        config = self.get_object()
        config.es_activa = True
        config.save()
        return Response({'message': 'Configuración activada'})

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """Desactiva una configuración de alerta."""
        config = self.get_object()
        config.es_activa = False
        config.save()
        return Response({'message': 'Configuración desactivada'})


class RegistrosMantenimientoSensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para registros de mantenimiento de sensores.
    """
    queryset = RegistrosMantenimientoSensor.objects.select_related(
        'dispositivo', 'registrado_por'
    ).all()
    serializer_class = RegistrosMantenimientoSensorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['dispositivo', 'tipo_mantenimiento']
    ordering_fields = ['fecha_mantenimiento']
    ordering = ['-fecha_mantenimiento']

    @action(detail=False, methods=['get'])
    def proximos(self, request):
        """Obtiene próximos mantenimientos programados."""
        dias = int(request.query_params.get('dias', 30))
        fecha_limite = timezone.now().date() + timedelta(days=dias)
        
        registros = self.queryset.filter(
            proximo_mantenimiento__lte=fecha_limite,
            proximo_mantenimiento__gte=timezone.now().date()
        )
        
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_dispositivo(self, request):
        """Obtiene historial de mantenimiento de un dispositivo."""
        dispositivo_id = request.query_params.get('dispositivo_id')
        if not dispositivo_id:
            return Response(
                {'error': 'Se requiere parámetro dispositivo_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registros = self.queryset.filter(dispositivo_id=dispositivo_id)
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)
