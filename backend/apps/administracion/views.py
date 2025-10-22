from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.administracion.models import ConfiguracionSistema, LogsAcceso, LogsActividad, BackupsSistema
from apps.administracion.serializers import (
    ConfiguracionSistemaSerializer, LogsAccesoSerializer, LogsActividadSerializer, BackupsSistemaSerializer
)


# Configuración
class ConfiguracionSistemaView(generics.RetrieveUpdateAPIView):
    """Obtener o actualizar configuración del sistema"""
    queryset = ConfiguracionSistema.objects.all()
    serializer_class = ConfiguracionSistemaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj, _ = ConfiguracionSistema.objects.get_or_create(id=1)
        return obj


# Logs Acceso
class LogsAccesoListView(generics.ListCreateAPIView):
    """Listar y crear logs de acceso"""
    queryset = LogsAcceso.objects.all()
    serializer_class = LogsAccesoSerializer
    permission_classes = [IsAuthenticated]


class LogsAccesoDetailView(generics.RetrieveAPIView):
    """Obtener log de acceso"""
    queryset = LogsAcceso.objects.all()
    serializer_class = LogsAccesoSerializer
    permission_classes = [IsAuthenticated]


# Logs Actividad
class LogsActividadListView(generics.ListCreateAPIView):
    """Listar y crear logs de actividad"""
    queryset = LogsActividad.objects.all()
    serializer_class = LogsActividadSerializer
    permission_classes = [IsAuthenticated]


class LogsActividadDetailView(generics.RetrieveAPIView):
    """Obtener log de actividad"""
    queryset = LogsActividad.objects.all()
    serializer_class = LogsActividadSerializer
    permission_classes = [IsAuthenticated]


# Backups
class BackupsSistemaListView(generics.ListCreateAPIView):
    """Listar y crear backups"""
    queryset = BackupsSistema.objects.all()
    serializer_class = BackupsSistemaSerializer
    permission_classes = [IsAuthenticated]


class BackupsSistemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar backup"""
    queryset = BackupsSistema.objects.all()
    serializer_class = BackupsSistemaSerializer
    permission_classes = [IsAuthenticated]


class EjecutarBackupView(generics.CreateAPIView):
    """Ejecutar backup del sistema"""
    serializer_class = BackupsSistemaSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Lógica para ejecutar backup
        return Response({'mensaje': 'Backup ejecutado exitosamente'}, status=status.HTTP_201_CREATED)
