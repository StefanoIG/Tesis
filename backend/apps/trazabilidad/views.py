from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from apps.trazabilidad.models import (
    Productos, Lotes, EventosTrazabilidad, TiposEventosTrazabilidad,
    HistorialEstadosLote
)
from apps.trazabilidad.serializers import (
    ProductoSerializer, LotesSerializer, LotesConEventosSerializer, EventosTrazabilidadSerializer,
    TiposEventosTrazabilidadSerializer, HistorialEstadosLoteSerializer
)


# Productos
class ProductosListView(generics.ListCreateAPIView):
    """Listar y crear productos"""
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]


class ProductosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar producto"""
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]


# Lotes
class LotesListView(generics.ListCreateAPIView):
    """Listar y crear lotes"""
    queryset = Lotes.objects.all().select_related('producto')
    serializer_class = LotesSerializer
    permission_classes = [IsAuthenticated]


class LotesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar lote"""
    queryset = Lotes.objects.all()
    serializer_class = LotesConEventosSerializer
    permission_classes = [IsAuthenticated]


class LotesEventosView(generics.ListCreateAPIView):
    """Listar y crear eventos de un lote"""
    serializer_class = EventosTrazabilidadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        lote_id = self.kwargs['pk']
        return EventosTrazabilidad.objects.filter(lote_id=lote_id)
    
    def perform_create(self, serializer):
        lote_id = self.kwargs['pk']
        serializer.save(lote_id=lote_id)


class LotesHistorialView(generics.ListAPIView):
    """Listar historial de cambios de estado de un lote"""
    serializer_class = HistorialEstadosLoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        lote_id = self.kwargs['pk']
        return HistorialEstadosLote.objects.filter(lote_id=lote_id)


class LotesGenerarQRView(generics.RetrieveAPIView):
    """Generar código QR para un lote"""
    queryset = Lotes.objects.all()
    serializer_class = LotesSerializer
    permission_classes = [IsAuthenticated]


# Tipos de Eventos
class TiposEventosListView(generics.ListCreateAPIView):
    """Listar y crear tipos de eventos"""
    queryset = TiposEventosTrazabilidad.objects.all()
    serializer_class = TiposEventosTrazabilidadSerializer
    permission_classes = [IsAuthenticated]


class TiposEventosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar tipo de evento"""
    queryset = TiposEventosTrazabilidad.objects.all()
    serializer_class = TiposEventosTrazabilidadSerializer
    permission_classes = [IsAuthenticated]


# Eventos
class EventosListView(generics.ListCreateAPIView):
    """Listar y crear eventos de trazabilidad"""
    queryset = EventosTrazabilidad.objects.all()
    serializer_class = EventosTrazabilidadSerializer
    permission_classes = [IsAuthenticated]


class EventosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar evento"""
    queryset = EventosTrazabilidad.objects.all()
    serializer_class = EventosTrazabilidadSerializer
    permission_classes = [IsAuthenticated]
