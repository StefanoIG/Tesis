from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    Clientes, Ventas, DetallesVenta, Cotizaciones,
    HistorialInteraccionesCliente
)
from .serializers import (
    ClientesSerializer, VentasSerializer, VentaCreateSerializer,
    DetallesVentaSerializer, CotizacionesSerializer,
    HistorialInteraccionesClienteSerializer
)


class ClientesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de clientes.
    """
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_cliente', 'categoria', 'pais', 'es_activo']
    search_fields = ['nombre_comercial', 'razon_social', 'identificacion_fiscal', 'email']
    ordering_fields = ['nombre_comercial', 'fecha_primer_contacto', 'creado_en']
    ordering = ['nombre_comercial']

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtiene clientes activos."""
        clientes = self.queryset.filter(es_activo=True)
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtiene estadísticas de un cliente."""
        cliente = self.get_object()
        
        ventas = cliente.ventas.filter(estado__in=['CONFIRMADA', 'ENVIADA', 'ENTREGADA', 'FACTURADA'])
        
        stats = {
            'total_ventas': ventas.count(),
            'total_monto_ventas': ventas.aggregate(Sum('total'))['total__sum'] or 0,
            'ultima_venta': ventas.first().fecha_venta if ventas.exists() else None,
            'cotizaciones_pendientes': cliente.cotizaciones.filter(
                estado__in=['ENVIADA', 'BORRADOR']
            ).count(),
            'total_interacciones': cliente.interacciones.count(),
            'seguimientos_pendientes': cliente.interacciones.filter(
                requiere_seguimiento=True,
                seguimiento_completado=False
            ).count()
        }
        
        return Response(stats)

    @action(detail=True, methods=['get'])
    def historial_compras(self, request, pk=None):
        """Obtiene historial de compras de un cliente."""
        cliente = self.get_object()
        ventas = cliente.ventas.all()
        serializer = VentasSerializer(ventas, many=True)
        return Response(serializer.data)


class VentasViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de ventas.
    """
    queryset = Ventas.objects.select_related(
        'cliente', 'vendedor', 'transporte_asignado'
    ).prefetch_related('detalles').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'vendedor', 'estado', 'condicion_pago']
    search_fields = ['numero_venta', 'numero_factura', 'cliente__nombre_comercial']
    ordering_fields = ['fecha_venta', 'total', 'numero_venta']
    ordering = ['-fecha_venta']

    def get_serializer_class(self):
        if self.action == 'create':
            return VentaCreateSerializer
        return VentasSerializer

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Obtiene ventas pendientes de entrega."""
        ventas = self.queryset.filter(estado__in=['CONFIRMADA', 'EN_PREPARACION', 'ENVIADA'])
        serializer = self.get_serializer(ventas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_estado(self, request):
        """Agrupa ventas por estado."""
        resumen = {}
        for estado_code, estado_name in Ventas.ESTADOS_VENTA:
            count = self.queryset.filter(estado=estado_code).count()
            total = self.queryset.filter(estado=estado_code).aggregate(Sum('total'))['total__sum'] or 0
            resumen[estado_code] = {
                'nombre': estado_name,
                'cantidad': count,
                'total': float(total)
            }
        return Response(resumen)

    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambia el estado de una venta."""
        venta = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if not nuevo_estado:
            return Response(
                {'error': 'Se requiere el campo estado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar que el estado existe
        estados_validos = [e[0] for e in Ventas.ESTADOS_VENTA]
        if nuevo_estado not in estados_validos:
            return Response(
                {'error': f'Estado inválido. Valores permitidos: {estados_validos}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        venta.estado = nuevo_estado
        
        # Actualizar fecha de entrega real si se marca como entregada
        if nuevo_estado == 'ENTREGADA' and not venta.fecha_entrega_real:
            venta.fecha_entrega_real = timezone.now().date()
        
        venta.save()
        
        serializer = self.get_serializer(venta)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtiene estadísticas generales de ventas."""
        # Filtros opcionales
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        
        queryset = self.queryset
        if fecha_desde:
            queryset = queryset.filter(fecha_venta__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_venta__lte=fecha_hasta)
        
        stats = {
            'total_ventas': queryset.count(),
            'total_monto': queryset.aggregate(Sum('total'))['total__sum'] or 0,
            'promedio_venta': queryset.aggregate(Sum('total'))['total__sum'] / queryset.count() if queryset.count() > 0 else 0,
            'por_estado': dict(
                queryset.values('estado').annotate(count=Count('id')).values_list('estado', 'count')
            ),
            'top_clientes': list(
                queryset.values('cliente__nombre_comercial')
                .annotate(total=Sum('total'), cantidad=Count('id'))
                .order_by('-total')[:10]
            )
        }
        
        return Response(stats)


class DetallesVentaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para detalles de venta.
    """
    queryset = DetallesVenta.objects.select_related('venta', 'lote').all()
    serializer_class = DetallesVentaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['venta', 'lote']


class CotizacionesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de cotizaciones.
    """
    queryset = Cotizaciones.objects.select_related(
        'cliente', 'vendedor', 'venta_generada'
    ).all()
    serializer_class = CotizacionesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'vendedor', 'estado']
    search_fields = ['numero_cotizacion', 'cliente__nombre_comercial']
    ordering_fields = ['fecha_cotizacion', 'fecha_validez']
    ordering = ['-fecha_cotizacion']

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Obtiene cotizaciones pendientes (enviadas y no vencidas)."""
        hoy = timezone.now().date()
        cotizaciones = self.queryset.filter(
            estado='ENVIADA',
            fecha_validez__gte=hoy
        )
        serializer = self.get_serializer(cotizaciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Obtiene cotizaciones vencidas."""
        hoy = timezone.now().date()
        cotizaciones = self.queryset.filter(
            estado='ENVIADA',
            fecha_validez__lt=hoy
        )
        # Marcar como vencidas
        cotizaciones.update(estado='VENCIDA')
        
        serializer = self.get_serializer(cotizaciones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def convertir_a_venta(self, request, pk=None):
        """Convierte una cotización en venta."""
        cotizacion = self.get_object()
        
        if cotizacion.estado != 'ACEPTADA':
            return Response(
                {'error': 'Solo se pueden convertir cotizaciones aceptadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if cotizacion.venta_generada:
            return Response(
                {'error': 'Esta cotización ya fue convertida a venta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear venta
        numero_venta = request.data.get('numero_venta')
        if not numero_venta:
            return Response(
                {'error': 'Se requiere numero_venta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        venta = Ventas.objects.create(
            numero_venta=numero_venta,
            cliente=cotizacion.cliente,
            vendedor=cotizacion.vendedor,
            fecha_venta=timezone.now().date(),
            estado='CONFIRMADA',
            total=cotizacion.total,
            moneda=cotizacion.moneda
        )
        
        cotizacion.venta_generada = venta
        cotizacion.estado = 'CONVERTIDA'
        cotizacion.save()
        
        return Response({
            'message': 'Cotización convertida exitosamente',
            'venta_id': str(venta.id),
            'numero_venta': venta.numero_venta
        })


class HistorialInteraccionesClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para historial de interacciones con clientes.
    """
    queryset = HistorialInteraccionesCliente.objects.select_related(
        'cliente', 'usuario'
    ).all()
    serializer_class = HistorialInteraccionesClienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'tipo_interaccion', 'requiere_seguimiento', 'seguimiento_completado']
    search_fields = ['asunto', 'descripcion']
    ordering_fields = ['fecha_interaccion']
    ordering = ['-fecha_interaccion']

    @action(detail=False, methods=['get'])
    def seguimientos_pendientes(self, request):
        """Obtiene interacciones con seguimiento pendiente."""
        interacciones = self.queryset.filter(
            requiere_seguimiento=True,
            seguimiento_completado=False
        )
        serializer = self.get_serializer(interacciones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def marcar_seguimiento_completado(self, request, pk=None):
        """Marca un seguimiento como completado."""
        interaccion = self.get_object()
        interaccion.seguimiento_completado = True
        interaccion.save()
        return Response({'message': 'Seguimiento marcado como completado'})

    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        """Obtiene interacciones de un cliente específico."""
        cliente_id = request.query_params.get('cliente_id')
        if not cliente_id:
            return Response(
                {'error': 'Se requiere parámetro cliente_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        interacciones = self.queryset.filter(cliente_id=cliente_id)
        serializer = self.get_serializer(interacciones, many=True)
        return Response(serializer.data)
