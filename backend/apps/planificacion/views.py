from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import date, timedelta

from .models import (
    EstudiosSuelo, Parcelas, CatalogosCultivos, PlanesCultivo,
    CalendariosRiego, RegistrosRiego, PermisosNacionalesEcuador, PermisosObtenidos
)
from .serializers import (
    EstudiosSueloSerializer, ParcelasSerializer, CatalogosCultivosSerializer,
    PlanesCultivoSerializer, CalendariosRiegoSerializer, RegistrosRiegoSerializer,
    PermisosNacionalesEcuadorSerializer, PermisosObtenidosSerializer
)


class EstudiosSueloViewSet(viewsets.ModelViewSet):
    queryset = EstudiosSuelo.objects.all()
    serializer_class = EstudiosSueloSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['finca', 'parcela', 'es_vigente']
    search_fields = ['nombre', 'laboratorio']
    ordering_fields = ['fecha_estudio', 'creado_en']
    ordering = ['-fecha_estudio']


class ParcelasViewSet(viewsets.ModelViewSet):
    queryset = Parcelas.objects.all()
    serializer_class = ParcelasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['finca', 'estado_parcela', 'cultivo_actual', 'es_activa']
    search_fields = ['nombre', 'codigo_parcela']
    ordering_fields = ['area_hectareas', 'creado_en']
    ordering = ['codigo_parcela']
    
    @action(detail=True, methods=['post'])
    def dividir_parcela(self, request, pk=None):
        """
        Divide una parcela en múltiples sub-parcelas.
        """
        parcela = self.get_object()
        divisiones = request.data.get('divisiones', [])
        
        if not divisiones:
            return Response(
                {'error': 'Debe proporcionar al menos una división'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        total_area = sum(d.get('area_hectareas', 0) for d in divisiones)
        if total_area > parcela.area_hectareas:
            return Response(
                {'error': 'La suma de áreas excede el área de la parcela original'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        nuevas_parcelas = []
        for i, division in enumerate(divisiones, 1):
            nueva_parcela = Parcelas.objects.create(
                finca=parcela.finca,
                codigo_parcela=f"{parcela.codigo_parcela}-{i}",
                nombre=division.get('nombre', f"{parcela.nombre} - Sub {i}"),
                area_hectareas=division.get('area_hectareas'),
                geometria_svg=division.get('geometria_svg', ''),
                coordenadas_geojson=division.get('coordenadas_geojson', {}),
                estado_parcela='DISPONIBLE'
            )
            nuevas_parcelas.append(nueva_parcela)
        
        # Marcar parcela original como inactiva
        parcela.es_activa = False
        parcela.save()
        
        serializer = self.get_serializer(nuevas_parcelas, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CatalogosCultivosViewSet(viewsets.ModelViewSet):
    queryset = CatalogosCultivos.objects.filter(es_activo=True)
    serializer_class = CatalogosCultivosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'nivel_dificultad', 'demanda_mercado']
    search_fields = ['nombre_comun', 'nombre_cientifico']
    ordering_fields = ['nombre_comun', 'dias_hasta_cosecha']
    ordering = ['nombre_comun']
    
    @action(detail=False, methods=['post'])
    def recomendar_cultivos(self, request):
        """
        Recomienda cultivos basándose en:
        - Estudio de suelo (si existe)
        - Prioridades del usuario (rentabilidad, facilidad, mercado)
        - Condiciones climáticas de la zona
        """
        parcela_id = request.data.get('parcela_id')
        prioridad = request.data.get('prioridad', 'rentabilidad')  # rentabilidad, facilidad, mercado
        
        if not parcela_id:
            return Response(
                {'error': 'Debe proporcionar el ID de la parcela'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            parcela = Parcelas.objects.get(id=parcela_id)
        except Parcelas.DoesNotExist:
            return Response(
                {'error': 'Parcela no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Obtener estudio de suelo más reciente (si existe)
        estudio_suelo = EstudiosSuelo.objects.filter(
            parcela=parcela,
            es_vigente=True
        ).order_by('-fecha_estudio').first()
        
        cultivos = CatalogosCultivos.objects.filter(es_activo=True)
        
        # Filtrar por compatibilidad de suelo
        if estudio_suelo and estudio_suelo.ph:
            cultivos = cultivos.filter(
                ph_minimo__lte=estudio_suelo.ph,
                ph_maximo__gte=estudio_suelo.ph
            )
            
            if estudio_suelo.textura:
                cultivos = cultivos.filter(
                    Q(texturas_compatibles__contains=[estudio_suelo.textura]) |
                    Q(texturas_compatibles=[])
                )
        
        # Ordenar según prioridad
        if prioridad == 'rentabilidad':
            cultivos = cultivos.order_by('-precio_mercado_promedio', '-rendimiento_promedio_hectarea')
        elif prioridad == 'facilidad':
            cultivos = cultivos.order_by('nivel_dificultad', 'dias_hasta_cosecha')
        elif prioridad == 'mercado':
            cultivos = cultivos.order_by('-demanda_mercado', '-precio_mercado_promedio')
        
        # Calcular score de compatibilidad
        recomendaciones = []
        for cultivo in cultivos[:10]:
            score = 0
            razones = []
            
            if estudio_suelo and estudio_suelo.ph:
                if cultivo.ph_optimo_min <= estudio_suelo.ph <= cultivo.ph_optimo_max:
                    score += 40
                    razones.append(f"pH óptimo ({estudio_suelo.ph})")
                elif cultivo.ph_minimo <= estudio_suelo.ph <= cultivo.ph_maximo:
                    score += 20
                    razones.append(f"pH aceptable ({estudio_suelo.ph})")
            
            if prioridad == 'rentabilidad' and cultivo.precio_mercado_promedio:
                score += 30
                razones.append(f"Alta rentabilidad (${cultivo.precio_mercado_promedio}/kg)")
            
            if cultivo.nivel_dificultad in ['FACIL', 'MODERADO']:
                score += 15
                razones.append(f"Dificultad: {cultivo.get_nivel_dificultad_display()}")
            
            if cultivo.demanda_mercado in ['ALTA', 'MUY_ALTA']:
                score += 15
                razones.append(f"Demanda: {cultivo.get_demanda_mercado_display()}")
            
            recomendaciones.append({
                'cultivo': CatalogosCultivosSerializer(cultivo).data,
                'score_compatibilidad': score,
                'razones': razones,
                'tiene_estudio_suelo': estudio_suelo is not None
            })
        
        return Response({
            'parcela': ParcelasSerializer(parcela).data,
            'estudio_suelo': EstudiosSueloSerializer(estudio_suelo).data if estudio_suelo else None,
            'prioridad': prioridad,
            'recomendaciones': sorted(recomendaciones, key=lambda x: x['score_compatibilidad'], reverse=True)
        })


class PlanesCultivoViewSet(viewsets.ModelViewSet):
    queryset = PlanesCultivo.objects.all()
    serializer_class = PlanesCultivoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parcela', 'cultivo', 'estado']
    search_fields = ['variedad']
    ordering_fields = ['fecha_planificada_siembra', 'progreso_porcentaje']
    ordering = ['-fecha_planificada_siembra']
    
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)


class CalendariosRiegoViewSet(viewsets.ModelViewSet):
    queryset = CalendariosRiego.objects.all()
    serializer_class = CalendariosRiegoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['plan_cultivo', 'tipo_riego', 'usa_sensores', 'es_activo']
    ordering_fields = ['frecuencia_dias']
    ordering = ['plan_cultivo']
    
    @action(detail=False, methods=['get'])
    def proximos_riegos(self, request):
        """
        Obtiene los próximos riegos programados en los siguientes 7 días.
        """
        from django.utils import timezone
        
        calendarios_activos = CalendariosRiego.objects.filter(es_activo=True)
        proximos = []
        
        hoy = timezone.now().date()
        
        for calendario in calendarios_activos:
            # Obtener último riego
            ultimo_riego = RegistrosRiego.objects.filter(
                calendario=calendario
            ).order_by('-fecha_hora_inicio').first()
            
            if ultimo_riego:
                proximo_riego = ultimo_riego.fecha_hora_inicio.date() + timedelta(days=calendario.frecuencia_dias)
            else:
                proximo_riego = hoy
            
            if proximo_riego <= hoy + timedelta(days=7):
                proximos.append({
                    'calendario': CalendariosRiegoSerializer(calendario).data,
                    'fecha_proximo_riego': proximo_riego,
                    'dias_restantes': (proximo_riego - hoy).days,
                    'vencido': proximo_riego < hoy
                })
        
        return Response(sorted(proximos, key=lambda x: x['fecha_proximo_riego']))


class RegistrosRiegoViewSet(viewsets.ModelViewSet):
    queryset = RegistrosRiego.objects.all()
    serializer_class = RegistrosRiegoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['calendario', 'tipo_ejecucion', 'ejecutado_por']
    ordering_fields = ['fecha_hora_inicio']
    ordering = ['-fecha_hora_inicio']
    
    def perform_create(self, serializer):
        if self.request.data.get('tipo_ejecucion') == 'MANUAL':
            serializer.save(ejecutado_por=self.request.user)
        else:
            serializer.save()


class PermisosNacionalesEcuadorViewSet(viewsets.ModelViewSet):
    queryset = PermisosNacionalesEcuador.objects.filter(es_activo=True)
    serializer_class = PermisosNacionalesEcuadorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_permiso', 'entidad_emisora', 'es_obligatorio']
    search_fields = ['nombre_permiso', 'codigo_permiso']
    ordering_fields = ['tiempo_tramite_dias', 'costo_estimado']
    ordering = ['entidad_emisora', 'nombre_permiso']
    
    @action(detail=False, methods=['post'])
    def permisos_para_cultivo(self, request):
        """
        Obtiene los permisos requeridos para un cultivo específico.
        """
        cultivo_id = request.data.get('cultivo_id')
        
        if not cultivo_id:
            return Response(
                {'error': 'Debe proporcionar el ID del cultivo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cultivo = CatalogosCultivos.objects.get(id=cultivo_id)
        except CatalogosCultivos.DoesNotExist:
            return Response(
                {'error': 'Cultivo no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Permisos específicos del cultivo
        permisos_especificos = PermisosNacionalesEcuador.objects.filter(
            cultivos_aplicables=cultivo,
            es_activo=True
        )
        
        # Permisos generales que aplican a todos
        permisos_generales = PermisosNacionalesEcuador.objects.filter(
            aplica_todo_cultivo=True,
            es_activo=True
        )
        
        permisos = (permisos_especificos | permisos_generales).distinct()
        
        serializer = self.get_serializer(permisos, many=True)
        return Response({
            'cultivo': CatalogosCultivosSerializer(cultivo).data,
            'permisos': serializer.data,
            'total_permisos': permisos.count()
        })


class PermisosObtenidosViewSet(viewsets.ModelViewSet):
    queryset = PermisosObtenidos.objects.all()
    serializer_class = PermisosObtenidosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'finca', 'permiso', 'estado']
    search_fields = ['numero_permiso']
    ordering_fields = ['fecha_emision', 'fecha_vencimiento']
    ordering = ['-fecha_emision']
    
    @action(detail=False, methods=['get'])
    def proximos_vencer(self, request):
        """
        Obtiene permisos que vencen en los próximos 30 días.
        """
        from django.utils import timezone
        
        hoy = timezone.now().date()
        fecha_limite = hoy + timedelta(days=30)
        
        permisos = PermisosObtenidos.objects.filter(
            estado='VIGENTE',
            fecha_vencimiento__gte=hoy,
            fecha_vencimiento__lte=fecha_limite
        ).order_by('fecha_vencimiento')
        
        serializer = self.get_serializer(permisos, many=True)
        return Response(serializer.data)
