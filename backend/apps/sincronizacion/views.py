from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.sincronizacion.models import (
    EstadosSincronizacion, ConflictosSincronizacion, RegistrosSincronizacion, ControlVersionesDB
)
from apps.sincronizacion.serializers import (
    EstadosSincronizacionSerializer, ConflictosSincronizacionSerializer,
    RegistrosSincronizacionSerializer, ControlVersionesDBSerializer
)


# Estados
class EstadosSincronizacionListView(generics.ListCreateAPIView):
    """Listar y crear estados de sincronización"""
    queryset = EstadosSincronizacion.objects.all()
    serializer_class = EstadosSincronizacionSerializer
    permission_classes = [IsAuthenticated]


class EstadosSincronizacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar estado"""
    queryset = EstadosSincronizacion.objects.all()
    serializer_class = EstadosSincronizacionSerializer
    permission_classes = [IsAuthenticated]


# Sincronización
class SincronizarView(generics.CreateAPIView):
    """Sincronizar base de datos"""
    serializer_class = EstadosSincronizacionSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Lógica de sincronización
        return Response({'mensaje': 'Sincronización iniciada'}, status=status.HTTP_201_CREATED)


class SincronizarUploadView(generics.CreateAPIView):
    """Subir cambios"""
    serializer_class = EstadosSincronizacionSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Lógica para subir cambios
        return Response({'mensaje': 'Cambios subidos exitosamente'}, status=status.HTTP_201_CREATED)


class SincronizarDownloadView(generics.CreateAPIView):
    """Descargar cambios"""
    serializer_class = EstadosSincronizacionSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Lógica para descargar cambios
        return Response({'mensaje': 'Cambios descargados exitosamente'}, status=status.HTTP_201_CREATED)


# Conflictos
class ConflictosListView(generics.ListCreateAPIView):
    """Listar y crear conflictos"""
    queryset = ConflictosSincronizacion.objects.all()
    serializer_class = ConflictosSincronizacionSerializer
    permission_classes = [IsAuthenticated]


class ConflictosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar conflicto"""
    queryset = ConflictosSincronizacion.objects.all()
    serializer_class = ConflictosSincronizacionSerializer
    permission_classes = [IsAuthenticated]


class ConflictosResolverView(generics.UpdateAPIView):
    """Resolver conflicto"""
    queryset = ConflictosSincronizacion.objects.all()
    serializer_class = ConflictosSincronizacionSerializer
    permission_classes = [IsAuthenticated]


# Registros
class RegistrosSincronizacionListView(generics.ListCreateAPIView):
    """Listar y crear registros de sincronización"""
    queryset = RegistrosSincronizacion.objects.all()
    serializer_class = RegistrosSincronizacionSerializer
    permission_classes = [IsAuthenticated]


class RegistrosSincronizacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar registro"""
    queryset = RegistrosSincronizacion.objects.all()
    serializer_class = RegistrosSincronizacionSerializer
    permission_classes = [IsAuthenticated]


# Versiones
class VersionesDBListView(generics.ListCreateAPIView):
    """Listar y crear versiones"""
    queryset = ControlVersionesDB.objects.all()
    serializer_class = ControlVersionesDBSerializer
    permission_classes = [IsAuthenticated]


class VersionesDBDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar versión"""
    queryset = ControlVersionesDB.objects.all()
    serializer_class = ControlVersionesDBSerializer
    permission_classes = [IsAuthenticated]
