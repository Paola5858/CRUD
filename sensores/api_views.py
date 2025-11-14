"""
API Views para integração externa do MOTOSENSE.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, Max, Min

from .models import Motor, Sensor, DadosSensor, EventoCritico
from .serializers import (
    MotorSerializer, SensorSerializer, DadosSensorSerializer,
    DadosSensorCreateSerializer, EventoCriticoSerializer,
    DashboardStatsSerializer
)


class MotorViewSet(viewsets.ModelViewSet):
    """API para gerenciamento de motores"""
    queryset = Motor.objects.filter(ativo=True)
    serializer_class = MotorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'potencia']
    search_fields = ['nome']
    ordering_fields = ['nome', 'potencia', 'criado_em']
    ordering = ['-criado_em']
    
    @action(detail=True, methods=['get'])
    def dados_recentes(self, request, pk=None):
        """Retorna dados recentes de um motor específico"""
        motor = self.get_object()
        dias = int(request.query_params.get('dias', 7))
        
        data_limite = timezone.now() - timedelta(days=dias)
        dados = DadosSensor.objects.filter(
            motor=motor,
            data_hora__gte=data_limite
        ).select_related('sensor').order_by('-data_hora')[:100]
        
        serializer = DadosSensorSerializer(dados, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        """Retorna estatísticas de um motor"""
        motor = self.get_object()
        dias = int(request.query_params.get('dias', 30))
        
        data_limite = timezone.now() - timedelta(days=dias)
        dados = DadosSensor.objects.filter(
            motor=motor,
            data_hora__gte=data_limite
        )
        
        stats = dados.aggregate(
            total_leituras=Count('id'),
            valor_medio=Avg('valor'),
            valor_min=Min('valor'),
            valor_max=Max('valor'),
            temp_media=Avg('temperatura'),
            temp_max=Max('temperatura'),
            rpm_medio=Avg('rpm'),
            rpm_max=Max('rpm')
        )
        
        return Response(stats)


class SensorViewSet(viewsets.ModelViewSet):
    """API para gerenciamento de sensores"""
    queryset = Sensor.objects.filter(ativo=True)
    serializer_class = SensorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tipo', 'ativo']
    search_fields = ['tipo']


class DadosSensorViewSet(viewsets.ModelViewSet):
    """API para dados de sensores"""
    queryset = DadosSensor.objects.select_related('motor', 'sensor')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['motor', 'sensor', 'fonte']
    ordering_fields = ['data_hora', 'valor']
    ordering = ['-data_hora']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DadosSensorCreateSerializer
        return DadosSensorSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros por data
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        
        if data_inicio:
            queryset = queryset.filter(data_hora__date__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_hora__date__lte=data_fim)
        
        # Filtro por valor
        valor_min = self.request.query_params.get('valor_min')
        valor_max = self.request.query_params.get('valor_max')
        
        if valor_min:
            queryset = queryset.filter(valor__gte=valor_min)
        if valor_max:
            queryset = queryset.filter(valor__lte=valor_max)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def resumo_diario(self, request):
        """Retorna resumo diário dos dados"""
        dias = int(request.query_params.get('dias', 7))
        data_limite = timezone.now() - timedelta(days=dias)
        
        dados = DadosSensor.objects.filter(
            data_hora__gte=data_limite
        ).extra(
            select={'dia': 'DATE(data_hora)'}
        ).values('dia').annotate(
            total_leituras=Count('id'),
            valor_medio=Avg('valor'),
            temp_media=Avg('temperatura'),
            rpm_medio=Avg('rpm')
        ).order_by('-dia')
        
        return Response(dados)


class EventoCriticoViewSet(viewsets.ReadOnlyModelViewSet):
    """API para eventos críticos (somente leitura)"""
    queryset = EventoCritico.objects.select_related('motor', 'sensor')
    serializer_class = EventoCriticoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['motor', 'sensor', 'tipo', 'resolvido']
    ordering = ['-data_hora']
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """Marca evento como resolvido"""
        evento = self.get_object()
        evento.resolvido = True
        evento.save()
        
        return Response({'status': 'Evento marcado como resolvido'})


class DashboardAPIView(viewsets.ViewSet):
    """API para dados do dashboard"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Retorna estatísticas gerais do sistema"""
        hoje = timezone.now().date()
        
        stats = {
            'total_motores': Motor.objects.filter(ativo=True).count(),
            'total_sensores': Sensor.objects.filter(ativo=True).count(),
            'motores_online': Motor.objects.filter(
                ativo=True,
                dados__data_hora__date=hoje
            ).distinct().count(),
            'dados_hoje': DadosSensor.objects.filter(
                data_hora__date=hoje
            ).count(),
            'alertas_ativos': EventoCritico.objects.filter(
                resolvido=False
            ).count(),
            'ultima_atualizacao': timezone.now()
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dados_tempo_real(self, request):
        """Retorna últimos dados para gráficos em tempo real"""
        limit = int(request.query_params.get('limit', 50))
        
        dados = DadosSensor.objects.select_related(
            'motor', 'sensor'
        ).order_by('-data_hora')[:limit]
        
        serializer = DadosSensorSerializer(dados, many=True)
        return Response(serializer.data)