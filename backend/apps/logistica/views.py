from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.logistica.models import Vehiculos, Conductores, Envios, RuteTrackingActual, AlertasLogistica
from apps.logistica.serializers import (
    VehiculosSerializer, ConductoresSerializer, EnviosSerializer, EnviosConDetallesSerializer,
    RuteTrackingActualSerializer, AlertasLogisticaSerializer
)


# Vehículos
class VehiculosListView(generics.ListCreateAPIView):
    """Listar y crear vehículos"""
    queryset = Vehiculos.objects.all()
    serializer_class = VehiculosSerializer
    permission_classes = [IsAuthenticated]


class VehiculosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar vehículo"""
    queryset = Vehiculos.objects.all()
    serializer_class = VehiculosSerializer
    permission_classes = [IsAuthenticated]


# Conductores
class ConductoresListView(generics.ListCreateAPIView):
    """Listar y crear conductores"""
    queryset = Conductores.objects.all()
    serializer_class = ConductoresSerializer
    permission_classes = [IsAuthenticated]


class ConductoresDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar conductor"""
    queryset = Conductores.objects.all()
    serializer_class = ConductoresSerializer
    permission_classes = [IsAuthenticated]


# Envíos
class EnviosListView(generics.ListCreateAPIView):
    """Listar y crear envíos"""
    queryset = Envios.objects.all()
    serializer_class = EnviosSerializer
    permission_classes = [IsAuthenticated]


class EnviosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar envío"""
    queryset = Envios.objects.all()
    serializer_class = EnviosConDetallesSerializer
    permission_classes = [IsAuthenticated]


# Tracking por Envío
class EnviosTrackingView(generics.ListAPIView):
    """Listar tracking para un envío específico"""
    serializer_class = RuteTrackingActualSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        envio_id = self.kwargs['pk']
        return RuteTrackingActual.objects.filter(envio_id=envio_id)


# Rastreo General
class TrackingListView(generics.ListCreateAPIView):
    """Listar y crear rastreos"""
    queryset = RuteTrackingActual.objects.all()
    serializer_class = RuteTrackingActualSerializer
    permission_classes = [IsAuthenticated]


class TrackingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar rastreo"""
    queryset = RuteTrackingActual.objects.all()
    serializer_class = RuteTrackingActualSerializer
    permission_classes = [IsAuthenticated]


# Alertas Logística
class AlertasLogisticaListView(generics.ListCreateAPIView):
    """Listar y crear alertas"""
    queryset = AlertasLogistica.objects.all()
    serializer_class = AlertasLogisticaSerializer
    permission_classes = [IsAuthenticated]


class AlertasLogisticaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar alerta"""
    queryset = AlertasLogistica.objects.all()
    serializer_class = AlertasLogisticaSerializer
    permission_classes = [IsAuthenticated]
