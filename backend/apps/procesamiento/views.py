from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.procesamiento.models import (
    ProcesosProcesamiento, InspeccionesCalidad, CertificacionesEstandares,
    ResultadosAnalisisLaboratorio
)
from apps.procesamiento.serializers import (
    ProcesosProcesimientoSerializer, InspeccionesCalidadSerializer,
    CertificacionesEstandaresSerializer, ResultadosAnalisisLaboratorioSerializer
)


# Procesos
class ProcesosProcesimientoListView(generics.ListCreateAPIView):
    """Listar y crear procesos"""
    queryset = ProcesosProcesamiento.objects.all()
    serializer_class = ProcesosProcesimientoSerializer
    permission_classes = [IsAuthenticated]


class ProcesosProcesimientoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar proceso"""
    queryset = ProcesosProcesamiento.objects.all()
    serializer_class = ProcesosProcesimientoSerializer
    permission_classes = [IsAuthenticated]


# Inspecciones
class InspeccionesCalidadListView(generics.ListCreateAPIView):
    """Listar y crear inspecciones"""
    queryset = InspeccionesCalidad.objects.all()
    serializer_class = InspeccionesCalidadSerializer
    permission_classes = [IsAuthenticated]


class InspeccionesCalidadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar inspección"""
    queryset = InspeccionesCalidad.objects.all()
    serializer_class = InspeccionesCalidadSerializer
    permission_classes = [IsAuthenticated]


# Certificaciones
class CertificacionesEstandaresListView(generics.ListCreateAPIView):
    """Listar y crear certificaciones"""
    queryset = CertificacionesEstandares.objects.all()
    serializer_class = CertificacionesEstandaresSerializer
    permission_classes = [IsAuthenticated]


class CertificacionesEstandaresDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar certificación"""
    queryset = CertificacionesEstandares.objects.all()
    serializer_class = CertificacionesEstandaresSerializer
    permission_classes = [IsAuthenticated]


# Análisis Laboratorio
class ResultadosAnalisisListView(generics.ListCreateAPIView):
    """Listar y crear análisis de laboratorio"""
    queryset = ResultadosAnalisisLaboratorio.objects.all()
    serializer_class = ResultadosAnalisisLaboratorioSerializer
    permission_classes = [IsAuthenticated]


class ResultadosAnalisisDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar análisis"""
    queryset = ResultadosAnalisisLaboratorio.objects.all()
    serializer_class = ResultadosAnalisisLaboratorioSerializer
    permission_classes = [IsAuthenticated]
