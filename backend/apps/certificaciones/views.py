from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from .models import (
    Certificaciones, CertificacionesProductores, CertificacionesLotes,
    RequisitosCumplimiento, CumplimientoNormativo
)
from .serializers import (
    CertificacionesSerializer, CertificacionesProductoresSerializer,
    CertificacionesLotesSerializer, RequisitosCumplimientoSerializer,
    CumplimientoNormativoSerializer
)


class CertificacionesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión del catálogo de certificaciones.
    """
    queryset = Certificaciones.objects.all()
    serializer_class = CertificacionesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_certificacion', 'alcance', 'es_activa']
    search_fields = ['nombre', 'codigo', 'entidad_emisora']
    ordering_fields = ['nombre', 'creado_en']
    ordering = ['nombre']


class CertificacionesProductoresViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de certificaciones de productores.
    """
    queryset = CertificacionesProductores.objects.select_related(
        'certificacion', 'productor', 'finca'
    ).all()
    serializer_class = CertificacionesProductoresSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['certificacion', 'productor', 'finca', 'estado']
    search_fields = ['numero_certificado', 'productor__nombre']
    ordering_fields = ['fecha_emision', 'fecha_expiracion']
    ordering = ['-fecha_emision']

    @action(detail=False, methods=['get'])
    def por_vencer(self, request):
        """Obtiene certificaciones próximas a vencer (90 días)."""
        fecha_limite = timezone.now().date() + timedelta(days=90)
        certificaciones = self.queryset.filter(
            estado='VIGENTE',
            fecha_expiracion__lte=fecha_limite,
            fecha_expiracion__gte=timezone.now().date()
        )
        serializer = self.get_serializer(certificaciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Obtiene certificaciones vencidas."""
        certificaciones = self.queryset.filter(
            fecha_expiracion__lt=timezone.now().date()
        )
        serializer = self.get_serializer(certificaciones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def renovar(self, request, pk=None):
        """Marca una certificación como renovada con nuevos datos."""
        certificacion = self.get_object()
        
        nueva_fecha_emision = request.data.get('fecha_emision')
        nueva_fecha_expiracion = request.data.get('fecha_expiracion')
        nuevo_numero = request.data.get('numero_certificado')
        
        if not all([nueva_fecha_emision, nueva_fecha_expiracion, nuevo_numero]):
            return Response(
                {'error': 'Se requieren fecha_emision, fecha_expiracion y numero_certificado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear nueva certificación renovada
        nueva_certificacion = CertificacionesProductores.objects.create(
            certificacion=certificacion.certificacion,
            productor=certificacion.productor,
            finca=certificacion.finca,
            numero_certificado=nuevo_numero,
            fecha_emision=nueva_fecha_emision,
            fecha_expiracion=nueva_fecha_expiracion,
            estado='VIGENTE',
            alcance_productos=certificacion.alcance_productos,
            alcance_procesos=certificacion.alcance_procesos
        )
        
        # Marcar la anterior como vencida
        certificacion.estado = 'VENCIDA'
        certificacion.save()
        
        serializer = self.get_serializer(nueva_certificacion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def actualizar_estados(self, request):
        """Actualiza el estado de todas las certificaciones según fecha."""
        actualizadas = 0
        for cert in self.queryset.filter(estado__in=['VIGENTE', 'POR_RENOVAR']):
            estado_anterior = cert.estado
            nuevo_estado = cert.actualizar_estado()
            if estado_anterior != nuevo_estado:
                cert.save()
                actualizadas += 1
        
        return Response({
            'message': f'{actualizadas} certificaciones actualizadas'
        })


class CertificacionesLotesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para vincular certificaciones con lotes.
    """
    queryset = CertificacionesLotes.objects.select_related(
        'lote', 'certificacion_productor__certificacion', 'verificado_por'
    ).all()
    serializer_class = CertificacionesLotesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lote', 'certificacion_productor', 'verificado']
    ordering_fields = ['creado_en']
    ordering = ['-creado_en']

    @action(detail=True, methods=['post'])
    def verificar(self, request, pk=None):
        """Marca una certificación de lote como verificada."""
        cert_lote = self.get_object()
        
        cert_lote.verificado = True
        cert_lote.verificado_por = request.user
        cert_lote.fecha_verificacion = timezone.now()
        cert_lote.observaciones = request.data.get('observaciones', '')
        cert_lote.save()
        
        serializer = self.get_serializer(cert_lote)
        return Response(serializer.data)


class RequisitosCumplimientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de requisitos de cumplimiento.
    """
    queryset = RequisitosCumplimiento.objects.select_related('certificacion').all()
    serializer_class = RequisitosCumplimientoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['certificacion', 'tipo_requisito', 'normativa', 'pais_destino', 'es_obligatorio']
    search_fields = ['codigo_requisito', 'nombre', 'normativa']
    ordering_fields = ['nombre']
    ordering = ['normativa', 'nombre']

    @action(detail=False, methods=['get'])
    def por_normativa(self, request):
        """Agrupa requisitos por normativa."""
        normativa = request.query_params.get('normativa')
        if not normativa:
            return Response(
                {'error': 'Se requiere parámetro normativa'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        requisitos = self.queryset.filter(normativa=normativa, es_activo=True)
        serializer = self.get_serializer(requisitos, many=True)
        return Response(serializer.data)


class CumplimientoNormativoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para registro de cumplimiento normativo.
    """
    queryset = CumplimientoNormativo.objects.select_related(
        'lote', 'requisito', 'verificado_por'
    ).all()
    serializer_class = CumplimientoNormativoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lote', 'requisito', 'cumplido']
    ordering_fields = ['fecha_verificacion']
    ordering = ['-fecha_verificacion']

    @action(detail=False, methods=['get'])
    def por_lote(self, request):
        """Obtiene todos los cumplimientos de un lote."""
        lote_id = request.query_params.get('lote_id')
        if not lote_id:
            return Response(
                {'error': 'Se requiere parámetro lote_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cumplimientos = self.queryset.filter(lote_id=lote_id)
        serializer = self.get_serializer(cumplimientos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen_lote(self, request):
        """Obtiene resumen de cumplimiento para un lote."""
        lote_id = request.query_params.get('lote_id')
        if not lote_id:
            return Response(
                {'error': 'Se requiere parámetro lote_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cumplimientos = self.queryset.filter(lote_id=lote_id)
        total = cumplimientos.count()
        cumplidos = cumplimientos.filter(cumplido=True).count()
        
        return Response({
            'total_requisitos': total,
            'cumplidos': cumplidos,
            'no_cumplidos': total - cumplidos,
            'porcentaje_cumplimiento': (cumplidos / total * 100) if total > 0 else 0
        })
