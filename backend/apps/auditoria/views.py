from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone

from .models import SesionesUsuario
from apps.autenticacion.models import Auditorias
from .serializers import AuditoriasSerializer, SesionesUsuarioSerializer


class AuditoriasViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consulta de registros de auditoría.
    Solo lectura para preservar integridad del log.
    """
    queryset = Auditorias.objects.select_related('usuario').all()
    serializer_class = AuditoriasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['usuario', 'entidad_afectada', 'accion', 'resultado']
    search_fields = ['accion', 'entidad_afectada', 'ip_origen']
    ordering_fields = ['timestamp', 'accion']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtiene estadísticas de auditoría."""
        # Últimas 24 horas
        hace_24h = timezone.now() - timedelta(hours=24)
        
        stats = {
            'total_registros': self.queryset.count(),
            'ultimas_24h': self.queryset.filter(timestamp__gte=hace_24h).count(),
            'por_resultado': dict(
                self.queryset.values('resultado').annotate(count=Count('id')).values_list('resultado', 'count')
            ),
            'acciones_mas_frecuentes': list(
                self.queryset.values('accion')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
                .values('accion', 'count')
            ),
            'usuarios_mas_activos': list(
                self.queryset.filter(usuario__isnull=False)
                .values('usuario__email', 'usuario__nombre_completo')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            )
        }
        
        return Response(stats)

    @action(detail=False, methods=['get'])
    def por_entidad(self, request):
        """Obtiene auditorías filtradas por entidad y registro_id."""
        entidad = request.query_params.get('entidad')
        registro_id = request.query_params.get('registro_id')
        
        if not entidad or not registro_id:
            return Response({'error': 'Se requieren parámetros entidad y registro_id'}, status=400)
        
        auditorias = self.queryset.filter(
            entidad_afectada=entidad,
            registro_id=registro_id
        ).order_by('timestamp')
        
        serializer = self.get_serializer(auditorias, many=True)
        return Response(serializer.data)


class SesionesUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consulta de sesiones de usuario.
    """
    queryset = SesionesUsuario.objects.select_related('usuario').all()
    serializer_class = SesionesUsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['usuario', 'estado', 'dispositivo']
    ordering_fields = ['fecha_inicio', 'fecha_ultima_actividad']
    ordering = ['-fecha_inicio']

    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Obtiene todas las sesiones activas."""
        sesiones = self.queryset.filter(estado='ACTIVA')
        serializer = self.get_serializer(sesiones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def mis_sesiones(self, request):
        """Obtiene las sesiones del usuario actual."""
        sesiones = self.queryset.filter(usuario=request.user)
        serializer = self.get_serializer(sesiones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cerrar_sesion(self, request, pk=None):
        """Cierra una sesión específica."""
        sesion = self.get_object()
        
        if sesion.estado == 'ACTIVA':
            sesion.estado = 'FORZADA_CIERRE'
            sesion.fecha_cierre = timezone.now()
            sesion.save()
            
            return Response({'message': 'Sesión cerrada exitosamente'})
        
        return Response({'error': 'La sesión no está activa'}, status=400)
