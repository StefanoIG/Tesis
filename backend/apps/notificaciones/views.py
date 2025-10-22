from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.notificaciones.models import Notificaciones, PreferenciasNotificaciones, HistorialLecturaNotifc
from apps.notificaciones.serializers import (
    NotificacionesSerializer, NotificacionesNoLeidasSerializer, PreferenciasNotificacionesSerializer, 
    HistorialLecturaNotificacionesSerializer
)


# Notificaciones
class NotificacionesNoLeidasView(generics.ListAPIView):
    """Listar notificaciones no leídas (para polling)"""
    serializer_class = NotificacionesNoLeidasSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtrar por usuario autenticado (necesita ser de tipo Usuarios)
        from apps.autenticacion.models import Usuarios
        try:
            usuario = Usuarios.objects.get(id=self.request.user.id)
            return Notificaciones.objects.filter(
                usuario_destinatario=usuario,
                fue_leida=False
            ).order_by('-creado_en')
        except Usuarios.DoesNotExist:
            return Notificaciones.objects.none()


class NotificacionesListView(generics.ListCreateAPIView):
    """Listar y crear notificaciones"""
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Auto-asignar usuario_destinatario si no viene en el request"""
        from apps.autenticacion.models import Usuarios
        try:
            usuario = Usuarios.objects.get(id=self.request.user.id)
            # Si viene usuario_destinatario en data, usarlo; sino usar el usuario autenticado
            usuario_destino = self.request.data.get('usuario_destinatario', usuario.id)
            serializer.save(usuario_destinatario_id=usuario_destino)
        except Usuarios.DoesNotExist:
            serializer.save(usuario_destinatario_id=self.request.data.get('usuario_destinatario'))


class NotificacionesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtener, actualizar y eliminar notificación"""
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer
    permission_classes = [IsAuthenticated]


class MarcarLeidaView(generics.UpdateAPIView):
    """Marcar notificación como leída"""
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer
    permission_classes = [IsAuthenticated]


class MarcarTodasLeidasView(generics.CreateAPIView):
    """Marcar todas las notificaciones como leídas"""
    serializer_class = NotificacionesSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        Notificaciones.objects.filter(
            usuario_destinatario=request.user,
            fue_leida=False
        ).update(fue_leida=True)
        return Response({'mensaje': 'Todas las notificaciones marcadas como leídas'}, status=status.HTTP_200_OK)


# Preferencias
class PreferenciasView(generics.RetrieveUpdateAPIView):
    """Obtener o actualizar preferencias de notificaciones"""
    serializer_class = PreferenciasNotificacionesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        from apps.autenticacion.models import Usuarios
        try:
            usuario = Usuarios.objects.get(id=self.request.user.id)
            obj, _ = PreferenciasNotificaciones.objects.get_or_create(usuario=usuario)
            return obj
        except Usuarios.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND("Usuario no encontrado")


# Historial
class HistorialLecturaListView(generics.ListCreateAPIView):
    """Listar historial de lectura"""
    queryset = HistorialLecturaNotifc.objects.all()
    serializer_class = HistorialLecturaNotificacionesSerializer
    permission_classes = [IsAuthenticated]
