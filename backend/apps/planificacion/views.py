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
    
    def create(self, request, *args, **kwargs):
        """
        Create soil study with PDF file upload.
        Accepts multipart/form-data with archivo_pdf field.
        """
        data = request.data.copy()
        
        # If no nombre provided, generate one
        if not data.get('nombre'):
            data['nombre'] = f"Estudio {data.get('finca', 'Finca')} - {date.today()}"
        
        # If no fecha_estudio, use today
        if not data.get('fecha_estudio'):
            data['fecha_estudio'] = date.today()
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ParcelasViewSet(viewsets.ModelViewSet):
    queryset = Parcelas.objects.all()
    serializer_class = ParcelasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['finca', 'estado_parcela', 'cultivo_actual', 'es_activa']
    search_fields = ['nombre', 'codigo_parcela']
    ordering_fields = ['area_hectareas', 'creado_en']
    ordering = ['codigo_parcela']
    
    @action(detail=False, methods=['get'])
    def por_finca(self, request):
        """
        Obtiene todas las parcelas de una finca específica.
        Query param: finca_id
        """
        finca_id = request.query_params.get('finca_id')
        
        if not finca_id:
            return Response(
                {'error': 'Debe proporcionar finca_id como query parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        parcelas = self.queryset.filter(finca_id=finca_id, es_activa=True)
        serializer = self.get_serializer(parcelas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def actualizar_geometria(self, request, pk=None):
        """
        Actualiza la geometría de una parcela con datos del mapa.
        """
        parcela = self.get_object()
        coordenadas_geojson = request.data.get('coordenadas_geojson')
        geometria_svg = request.data.get('geometria_svg', '')
        
        if coordenadas_geojson:
            parcela.coordenadas_geojson = coordenadas_geojson
            parcela.geometria_svg = geometria_svg
            parcela.save()
            
            return Response(
                ParcelasSerializer(parcela).data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'error': 'Debe proporcionar coordenadas_geojson'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
        - Preferencia de cultivo del productor
        - Zona geográfica seleccionada
        """
        parcela_ids = request.data.get('parcela_ids', [])
        if not parcela_ids and request.data.get('parcela_id'):
            parcela_ids = [request.data.get('parcela_id')]
        
        prioridad = request.data.get('prioridad', 'rentabilidad')  # rentabilidad, facilidad, mercado
        cultivo_preferido = request.data.get('cultivo_preferido')  # nombre del cultivo que quiere el productor
        area_geografica = request.data.get('area_geografica')  # GeoJSON del área seleccionada en el mapa
        
        if not parcela_ids:
            return Response(
                {'error': 'Debe proporcionar al menos una parcela'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            parcelas = Parcelas.objects.filter(id__in=parcela_ids)
            if not parcelas.exists():
                raise Parcelas.DoesNotExist
        except Parcelas.DoesNotExist:
            return Response(
                {'error': 'Parcelas no encontradas'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Obtener estudios de suelo para las parcelas seleccionadas
        estudios_suelo = []
        for parcela in parcelas:
            estudio = EstudiosSuelo.objects.filter(
                parcela=parcela,
                es_vigente=True
            ).order_by('-fecha_estudio').first()
            if estudio:
                estudios_suelo.append({'parcela': parcela, 'estudio': estudio})
        
        tiene_estudios = len(estudios_suelo) > 0
        
        # Iniciar con todos los cultivos activos
        cultivos = CatalogosCultivos.objects.filter(es_activo=True)
        
        # Si el productor tiene preferencia de cultivo, priorizarlo
        cultivo_usuario_obj = None
        if cultivo_preferido:
            cultivo_usuario_obj = CatalogosCultivos.objects.filter(
                Q(nombre_comun__icontains=cultivo_preferido) |
                Q(nombre_cientifico__icontains=cultivo_preferido)
            ).first()
        
        # Filtrar por compatibilidad de suelo si hay estudios
        if tiene_estudios:
            # Usar el primer estudio como referencia (podría promediar si hay varios)
            estudio_ref = estudios_suelo[0]['estudio']
            
            if estudio_ref.ph:
                cultivos = cultivos.filter(
                    ph_minimo__lte=estudio_ref.ph,
                    ph_maximo__gte=estudio_ref.ph
                )
                
                if estudio_ref.textura:
                    cultivos = cultivos.filter(
                        Q(texturas_compatibles__contains=[estudio_ref.textura]) |
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
        for cultivo in cultivos[:15]:
            score = 0
            razones = []
            zona_recomendada = None
            
            # BONUS: Si es el cultivo preferido del usuario
            if cultivo_usuario_obj and cultivo.id == cultivo_usuario_obj.id:
                score += 50
                razones.append("Cultivo preferido del productor")
            
            # Evaluar compatibilidad con estudios de suelo
            if tiene_estudios:
                for item in estudios_suelo:
                    estudio = item['estudio']
                    parcela_est = item['parcela']
                    
                    if estudio.ph:
                        if cultivo.ph_optimo_min <= estudio.ph <= cultivo.ph_optimo_max:
                            score += 40
                            razones.append(f"pH óptimo en {parcela_est.nombre} ({estudio.ph})")
                            zona_recomendada = parcela_est.nombre
                        elif cultivo.ph_minimo <= estudio.ph <= cultivo.ph_maximo:
                            score += 20
                            razones.append(f"pH aceptable en {parcela_est.nombre} ({estudio.ph})")
            
            # Evaluar según prioridad del usuario
            if prioridad == 'rentabilidad' and cultivo.precio_mercado_promedio:
                score += 30
                razones.append(f"Alta rentabilidad (${cultivo.precio_mercado_promedio}/kg)")
            
            if cultivo.nivel_dificultad in ['FACIL', 'MODERADO']:
                score += 15
                razones.append(f"Dificultad: {cultivo.get_nivel_dificultad_display()}")
            
            if cultivo.demanda_mercado in ['ALTA', 'MUY_ALTA']:
                score += 15
                razones.append(f"Demanda: {cultivo.get_demanda_mercado_display()}")
            
            # Si NO hay estudio de suelo pero el usuario quiere este cultivo, sugerir zona
            if not tiene_estudios and cultivo_usuario_obj and cultivo.id == cultivo_usuario_obj.id:
                # Sugerir la parcela más grande o primera disponible
                parcela_sugerida = parcelas.filter(estado_parcela='DISPONIBLE').order_by('-area_hectareas').first()
                if parcela_sugerida:
                    zona_recomendada = parcela_sugerida.nombre
                    razones.append(f"Zona sugerida: {zona_recomendada} (parcela disponible más amplia)")
            
            recomendaciones.append({
                'cultivo': CatalogosCultivosSerializer(cultivo).data,
                'score_compatibilidad': score,
                'razones': razones,
                'zona_recomendada': zona_recomendada,
                'tiene_estudio_suelo': tiene_estudios
            })
        
        return Response({
            'parcelas': ParcelasSerializer(parcelas, many=True).data,
            'estudios_suelo': [{'parcela': e['parcela'].nombre, 'estudio': EstudiosSueloSerializer(e['estudio']).data} for e in estudios_suelo],
            'tiene_estudios_suelo': tiene_estudios,
            'cultivo_preferido': CatalogosCultivosSerializer(cultivo_usuario_obj).data if cultivo_usuario_obj else None,
            'prioridad': prioridad,
            'area_geografica': area_geografica,
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
    
    @action(detail=False, methods=['post'])
    def crear_plan_automatico(self, request):
        """
        Crea un plan de cultivo automáticamente basándose en:
        - Parcela seleccionada
        - Cultivo recomendado o preferido
        - Fecha de inicio
        """
        parcela_id = request.data.get('parcela_id')
        cultivo_id = request.data.get('cultivo_id')
        fecha_inicio = request.data.get('fecha_inicio', date.today())
        variedad = request.data.get('variedad', '')
        
        if not parcela_id or not cultivo_id:
            return Response(
                {'error': 'Debe proporcionar parcela_id y cultivo_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            parcela = Parcelas.objects.get(id=parcela_id)
            cultivo = CatalogosCultivos.objects.get(id=cultivo_id)
        except (Parcelas.DoesNotExist, CatalogosCultivos.DoesNotExist) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calcular fecha estimada de cosecha
        if isinstance(fecha_inicio, str):
            from datetime import datetime
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        
        fecha_cosecha = fecha_inicio + timedelta(days=cultivo.dias_hasta_cosecha)
        
        # Crear el plan
        plan = PlanesCultivo.objects.create(
            parcela=parcela,
            cultivo=cultivo,
            variedad=variedad,
            fecha_planificada_siembra=fecha_inicio,
            fecha_estimada_cosecha=fecha_cosecha,
            estado='APROBADO',
            creado_por=request.user
        )
        
        # Actualizar estado de la parcela
        parcela.estado_parcela = 'EN_USO'
        parcela.save()
        
        return Response(
            PlanesCultivoSerializer(plan).data,
            status=status.HTTP_201_CREATED
        )


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
