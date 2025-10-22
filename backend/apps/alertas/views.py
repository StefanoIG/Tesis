from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.alertas.models import ReglasAlertas, Alertas
from apps.alertas.serializers import ReglasAlertasSerializer, AlertasSerializer


# Reglas
class ReglasAlertasListView(generics.ListCreateAPIView):
    """Listar y crear reglas de alertas"""
    queryset = ReglasAlertas.objects.all()
    serializer_class = ReglasAlertasSerializer
    permission_classes = [IsAuthenticated]


class ReglasAlertasDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar regla"""
    queryset = ReglasAlertas.objects.all()
    serializer_class = ReglasAlertasSerializer
    permission_classes = [IsAuthenticated]


# Alertas
class AlertasListView(generics.ListCreateAPIView):
    """Listar y crear alertas"""
    queryset = Alertas.objects.all()
    serializer_class = AlertasSerializer
    permission_classes = [IsAuthenticated]


class AlertasDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar alerta"""
    queryset = Alertas.objects.all()
    serializer_class = AlertasSerializer
    permission_classes = [IsAuthenticated]


class AlertasResolverView(generics.UpdateAPIView):
    """Resolver alerta"""
    queryset = Alertas.objects.all()
    serializer_class = AlertasSerializer
    permission_classes = [IsAuthenticated]


class AlertasAbiertasView(generics.ListAPIView):
    """Listar alertas abiertas"""
    serializer_class = AlertasSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Alertas.objects.filter(estado='ABIERTA')
