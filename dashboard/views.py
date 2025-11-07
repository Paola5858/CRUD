from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, Max, Min, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from datetime import datetime, timedelta
from sensores.models import Motor, Sensor, DadosSensor
import random


def dashboard_view(request):
    """View principal do dashboard com dados contextuais"""
    
    # Métricas básicas para o template
    context = {
        'total_motores': Motor.objects.count() or 12,
        'total_sensores': Sensor.objects.count() or 24,
        'total_leituras': DadosSensor.objects.count() or 15847,
        'motores_online': (Motor.objects.count() or 12) - random.randint(0, 4),
        'alertas_criticos': random.randint(1, 5),
        'temperatura_media': round(random.uniform(75, 85), 1),
        'rpm_medio': random.randint(3200, 3800),
        'uptime_sistema': round(random.uniform(98.5, 99.9), 1),
        'potencia_total': round(random.uniform(20, 30), 1)
    }
    
    return render(request, 'dashboard/index.html', context)


@cache_page(60 * 5)  # Cache por 5 minutos
@vary_on_headers('User-Agent')
def dashboard_metrics_api(request):
    """API principal para métricas do dashboard"""
    
    # Buscar dados reais dos últimos 12 meses
    hoje = timezone.now()
    doze_meses_atras = hoje - timedelta(days=365)
    
    # Agregar leituras por mês
    leituras_mensais = DadosSensor.objects.filter(
        data_hora__gte=doze_meses_atras
    ).annotate(
        mes=TruncMonth('data_hora')
    ).values('mes').annotate(
        temp_media=Avg('valor', filter=Q(sensor__tipo='TEMPERATURA')),
        press_media=Avg('valor', filter=Q(sensor__tipo='PRESSAO')),
        vel_media=Avg('valor', filter=Q(sensor__tipo='VELOCIDADE'))
    ).order_by('mes')
    
    # Converter para listas
    chart_data_temp = [float(r['temp_media'] or 0) for r in leituras_mensais]
    chart_data_press = [float(r['press_media'] or 0) for r in leituras_mensais]
    chart_data_vel = [float(r['vel_media'] or 0) for r in leituras_mensais]
    
    # Se não há dados suficientes, usar simulados como fallback
    if len(chart_data_temp) < 12:
        chart_data_temp = [15, 18, 22, 28, 24, 30, 38, 32, 35, 40, 42, 45]
        chart_data_press = [12, 15, 18, 24, 20, 25, 32, 28, 30, 35, 38, 40]
        chart_data_vel = [10, 13, 16, 22, 18, 23, 30, 26, 28, 33, 36, 38]
    
    labels = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    
    # Dados semanais para gráfico de barras
    weekly_data = {
        'labels': ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB', 'DOM'],
        'temperatura': [12000, 15000, 18000, 22000, 35000, 28000, 16000],
        'pressao': [8000, 12000, 14000, 18000, 28000, 22000, 12000],
        'velocidade': [10000, 13000, 16000, 20000, 32000, 25000, 14000]
    }
    
    # Métricas gerais
    total_motores = Motor.objects.count() or 12
    total_sensores = Sensor.objects.count() or 24
    total_leituras = DadosSensor.objects.count() or 15847
    
    # Distribuição de sensores
    sensor_distribution = [
        {'tipo': 'Temperatura', 'count': 12, 'percentage': 35},
        {'tipo': 'Pressão', 'count': 6, 'percentage': 25},
        {'tipo': 'Velocidade', 'count': 6, 'percentage': 40}
    ]
    
    return JsonResponse({
        'chart_main': {
            'labels': labels,
            'temperatura': chart_data_temp,
            'pressao': chart_data_press,
            'velocidade': chart_data_vel
        },
        'weekly_performance': weekly_data,
        'metrics': {
            'total_motores': total_motores,
            'total_sensores': total_sensores,
            'total_leituras': total_leituras,
            'crescimento': 47.8,
            'potencia_media': 1847,
            'uptime': 99.2,
            'temperatura_media': 78,
            'rpm_medio': 3450,
            'alertas_criticos': 3
        },
        'sensor_distribution': sensor_distribution,
        'gauge_value': 92,
        'status': 'success'
    })


@cache_page(60 * 2)  # Cache por 2 minutos
def motor_status_api(request):
    """Status dos motores em tempo real"""
    
    # Dados simulados para demonstração
    motor_status = [
        {'nome': 'Motor A1', 'potencia': 1500, 'temperatura': 85, 'online': True},
        {'nome': 'Motor B2', 'potencia': 1200, 'temperatura': 78, 'online': True},
        {'nome': 'Motor C3', 'potencia': 1800, 'temperatura': 92, 'online': True},
        {'nome': 'Motor D4', 'potencia': 0, 'temperatura': 0, 'online': False},
        {'nome': 'Motor E5', 'potencia': 1650, 'temperatura': 88, 'online': True},
        {'nome': 'Motor F6', 'potencia': 1400, 'temperatura': 81, 'online': True}
    ]
    
    # Se existem motores reais no banco, usar alguns dados reais (otimizado)
    motores_db = Motor.objects.only('nome', 'potencia')[:6]
    if motores_db:
        for i, motor in enumerate(motores_db):
            if i < len(motor_status):
                motor_status[i]['nome'] = motor.nome
                motor_status[i]['potencia'] = int(motor.potencia) if motor_status[i]['online'] else 0
    
    return JsonResponse({
        'motores': motor_status,
        'online_count': sum(1 for m in motor_status if m['online']),
        'status': 'success'
    })


@cache_page(60 * 1)  # Cache por 1 minuto
def alerts_api(request):
    """API para alertas críticos"""
    
    alerts = [
        {
            'tipo': 'critical',
            'icon': '🔥',
            'titulo': 'TEMPERATURA CRÍTICA',
            'detalhes': 'Motor D4 • 98°C',
            'timestamp': 'Há 2 min'
        },
        {
            'tipo': 'warning',
            'icon': '⚠️',
            'titulo': 'PRESSÃO ELEVADA',
            'detalhes': 'Sensor P2 • 4.2 bar',
            'timestamp': 'Há 5 min'
        },
        {
            'tipo': 'warning',
            'icon': '🔋',
            'titulo': 'BATERIA BAIXA',
            'detalhes': 'Sensor V3 • 15%',
            'timestamp': 'Há 12 min'
        }
    ]
    
    return JsonResponse({
        'alerts': alerts,
        'count': len(alerts),
        'status': 'success'
    })