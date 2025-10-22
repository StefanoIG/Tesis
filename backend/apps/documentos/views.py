from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.documentos.models import Documentos, FotosProductos
from apps.documentos.serializers import DocumentosSerializer, FotosProductosSerializer


# Documentos
class DocumentosListView(generics.ListCreateAPIView):
    """Listar y crear documentos"""
    queryset = Documentos.objects.all()
    serializer_class = DocumentosSerializer
    permission_classes = [IsAuthenticated]


class DocumentosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar documento"""
    queryset = Documentos.objects.all()
    serializer_class = DocumentosSerializer
    permission_classes = [IsAuthenticated]


class DocumentosValidarView(generics.UpdateAPIView):
    """Validar documento"""
    queryset = Documentos.objects.all()
    serializer_class = DocumentosSerializer
    permission_classes = [IsAuthenticated]


class DocumentosDescargarView(generics.RetrieveAPIView):
    """Descargar documento"""
    queryset = Documentos.objects.all()
    serializer_class = DocumentosSerializer
    permission_classes = [IsAuthenticated]


# Fotos
class FotosProductosListView(generics.ListCreateAPIView):
    """Listar y crear fotos"""
    queryset = FotosProductos.objects.all()
    serializer_class = FotosProductosSerializer
    permission_classes = [IsAuthenticated]


class FotosProductosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar foto"""
    queryset = FotosProductos.objects.all()
    serializer_class = FotosProductosSerializer
    permission_classes = [IsAuthenticated]
