"""
Otimizações de performance para o sistema MOTOSENSE.

Este módulo contém funções e classes para otimizar
queries, cache e performance geral do sistema.
"""

from django.db.models import Prefetch, Count, Avg, Max, Min
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Motor, Sensor, DadosSensor, SensorMotor


@login_required
@cache_page(60 * 5)  # Cache de 5 minutos
def dashboard_optimized(request):
    """
    Dashboard com queries otimizadas e cache.
    
    Otimizações aplicadas:
    - select_related() para ForeignKeys
    - prefetch_related() para ManyToMany
    - annotate() para agregações
    - Cache de 5 minutos
    - Limitação de registros (.only())
    """
    
    # Cache de KPIs (renovado a cada 5 min)
    cache_key = 'dashboard_kpis'
    kpis = cache.get(cache_key)
    
    if not kpis:
        kpis = {
            'total_motores': Motor.objects.count(),
            'total_sensores': Sensor.objects.count(),
            'media_leituras': DadosSensor.objects.aggregate(
                Avg('valor')
            )['valor__avg'] or 0,
            'leituras_hoje': DadosSensor.objects.filter(
                data_hora__date=timezone.now().date()
            ).count()
        }
        cache.set(cache_key, kpis, 300)  # 5 minutos
    
    # Query otimizada com select_related
    ultimos_dados = DadosSensor.objects.select_related(
        'motor', 'sensor'
    ).only(
        'id', 'data_hora', 'valor',
        'motor__nome', 'sensor__tipo'
    ).order_by('-data_hora')[:10]
    
    # Prefetch para evitar N+1 em relações many-to-many
    motores_com_sensores = Motor.objects.prefetch_related(
        Prefetch(
            'sensormotor_set',
            queryset=SensorMotor.objects.select_related('sensor')
        )
    ).annotate(
        total_leituras=Count('dados')
    )[:5]
    
    context = {
        **kpis,
        'ultimos_dados': ultimos_dados,
        'motores_com_sensores': motores_com_sensores,
    }
    
    return context


def clear_dashboard_cache():
    """Limpa cache do dashboard quando dados são atualizados"""
    cache.delete('dashboard_kpis')
    cache.delete_many(['dashboard_*'])


class QueryOptimizer:
    """Classe para otimização de queries comuns"""
    
    @staticmethod
    def get_motors_with_sensors():
        """Retorna motores com sensores otimizado"""
        return Motor.objects.select_related().prefetch_related(
            'sensormotor_set__sensor'
        ).annotate(
            sensor_count=Count('sensormotor')
        )
    
    @staticmethod
    def get_recent_data(limit=50):
        """Retorna dados recentes otimizado"""
        return DadosSensor.objects.select_related(
            'motor', 'sensor'
        ).order_by('-data_hora')[:limit]