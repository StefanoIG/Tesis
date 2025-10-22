from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.reportes.models import Reportes, IndicesKPI, DashboardDatos
from apps.reportes.serializers import ReportesSerializer, IndicesKPISerializer, DashboardDatosSerializer


# Reportes
class ReportesListView(generics.ListCreateAPIView):
    """Listar y crear reportes"""
    queryset = Reportes.objects.all()
    serializer_class = ReportesSerializer
    permission_classes = [IsAuthenticated]


class ReportesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar reporte"""
    queryset = Reportes.objects.all()
    serializer_class = ReportesSerializer
    permission_classes = [IsAuthenticated]


class ReportesDescargarView(generics.RetrieveAPIView):
    """Descargar reporte"""
    queryset = Reportes.objects.all()
    serializer_class = ReportesSerializer
    permission_classes = [IsAuthenticated]


class GenerarReporteTrazabilidadView(generics.CreateAPIView):
    """Generar reporte de trazabilidad"""
    serializer_class = ReportesSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Lógica para generar reporte
        return Response({'mensaje': 'Reporte de trazabilidad generado'}, status=status.HTTP_201_CREATED)


# KPIs
class IndicesKPIListView(generics.ListCreateAPIView):
    """Listar y crear KPIs"""
    queryset = IndicesKPI.objects.all()
    serializer_class = IndicesKPISerializer
    permission_classes = [IsAuthenticated]


class IndicesKPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar KPI"""
    queryset = IndicesKPI.objects.all()
    serializer_class = IndicesKPISerializer
    permission_classes = [IsAuthenticated]


# Dashboards
class DashboardDatosListView(generics.ListCreateAPIView):
    """Listar y crear dashboards"""
    queryset = DashboardDatos.objects.all()
    serializer_class = DashboardDatosSerializer
    permission_classes = [IsAuthenticated]


class DashboardDatosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar dashboard"""
    queryset = DashboardDatos.objects.all()
    serializer_class = DashboardDatosSerializer
    permission_classes = [IsAuthenticated]


class MiDashboardView(generics.ListAPIView):
    """Obtener dashboard del usuario actual"""
    serializer_class = DashboardDatosSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Retorna el dashboard del usuario actual (si existe)
        return DashboardDatos.objects.filter(usuario=self.request.user)[:1]
