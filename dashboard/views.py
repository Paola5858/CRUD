from django.shortcuts import render
from django.db.models import Avg, Sum, Q
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from sensores.models import Motor, Sensor, DadosSensor, SensorMotor
import json

def get_real_chart_data():
    """Obter dados reais para gráficos ou fallback"""
    hoje = timezone.now()
    doze_meses_atras = hoje - timedelta(days=365)
    
    dados_mensais = DadosSensor.objects.filter(
        data_hora__gte=doze_meses_atras
    ).annotate(
        mes=TruncMonth('data_hora')
    ).values('mes').annotate(
        temperatura=Avg('valor', filter=Q(sensor__tipo__iexact='TEMPERATURA')),
        pressao=Avg('valor', filter=Q(sensor__tipo__iexact='PRESSAO')),
        velocidade=Avg('valor', filter=Q(sensor__tipo__iexact='VELOCIDADE'))
    ).order_by('mes')
    
    labels = []
    temp_data = []
    press_data = []
    vel_data = []

    if dados_mensais.count() > 0:
        for dado in dados_mensais:
            labels.append(dado['mes'].strftime('%b').upper())
            temp_data.append(round(dado['temperatura'] or 0, 1))
            press_data.append(round(dado['pressao'] or 0, 1))
            vel_data.append(round(dado['velocidade'] or 0, 1))

    # Fallback para garantir 12 meses de dados para o gráfico
    while len(labels) < 12:
        last_month = datetime.strptime(labels[-1], '%b') if labels else hoje
        next_month = (last_month + timedelta(days=32)).strftime('%b').upper()
        labels.append(next_month)
        temp_data.append(temp_data[-1] * 0.95 if temp_data else 25)
        press_data.append(press_data[-1] * 0.95 if press_data else 20)
        vel_data.append(vel_data[-1] * 0.95 if vel_data else 15)

    return {'labels': labels[:12], 'temperatura': temp_data[:12], 'pressao': press_data[:12], 'velocidade': vel_data[:12]}

def get_weekly_performance_data():
    """Calcula o desempenho semanal dos sensores."""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    
    weekly_data = DadosSensor.objects.filter(
        data_hora__date__gte=start_of_week
    ).annotate(
        dia=TruncDay('data_hora')
    ).values('dia').annotate(
        temperatura=Sum('valor', filter=Q(sensor__tipo__iexact='TEMPERATURA')),
        pressao=Sum('valor', filter=Q(sensor__tipo__iexact='PRESSAO')),
        velocidade=Sum('valor', filter=Q(sensor__tipo__iexact='VELOCIDADE'))
    ).order_by('dia')

    labels = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB', 'DOM']
    temp_data = [0] * 7
    press_data = [0] * 7
    vel_data = [0] * 7

    for entry in weekly_data:
        day_index = entry['dia'].weekday()
        temp_data[day_index] = round(entry['temperatura'] or 0, 1)
        press_data[day_index] = round(entry['pressao'] or 0, 1)
        vel_data[day_index] = round(entry['velocidade'] or 0, 1)

    return {'labels': labels, 'temperatura': temp_data, 'pressao': press_data, 'velocidade': vel_data}

def calculate_growth_rate():
    """Calcular taxa de crescimento baseada em dados reais"""
    hoje = timezone.now()
    mes_passado = hoje - timedelta(days=30)
    
    leituras_mes_atual = DadosSensor.objects.filter(data_hora__gte=mes_passado).count()
    leituras_mes_anterior = DadosSensor.objects.filter(
        data_hora__gte=mes_passado - timedelta(days=30),
        data_hora__lt=mes_passado
    ).count()
    
    if leituras_mes_anterior > 0:
        return round(((leituras_mes_atual - leituras_mes_anterior) / leituras_mes_anterior) * 100, 1)
    return 0  # Retorna 0 se não houver dados anteriores

@login_required
def dashboard_view(request):
    """Dashboard com dados reais usando QuerySet conforme requisito"""
    
    total_motores = Motor.objects.count()
    total_sensores = Sensor.objects.count()
    total_sensor_motor = SensorMotor.objects.count()
    ultimos_dados = DadosSensor.objects.select_related('motor', 'sensor').order_by('-data_hora')[:10]
    total_leituras = DadosSensor.objects.count()

    potencia_total = Motor.objects.aggregate(total=Sum('potencia'))['total'] or 0
    temp_media = DadosSensor.objects.filter(sensor__tipo__iexact='TEMPERATURA').aggregate(media=Avg('valor'))['media']
    
    alertas_criticos = DadosSensor.objects.filter(valor__gt=90, sensor__tipo__iexact='TEMPERATURA').count()

    recent_time = timezone.now() - timedelta(hours=24)
    motores_online = DadosSensor.objects.filter(data_hora__gte=recent_time).values('motor').distinct().count()
    
    system_health = (motores_online / total_motores * 100) if total_motores > 0 else 0
    growth_rate = calculate_growth_rate()

    # Dados para os gráficos
    chart_data = get_real_chart_data()
    weekly_performance = get_weekly_performance_data()

    dashboard_data = {
        'metrics': {
            'total_motores': total_motores,
            'total_sensores': total_sensores,
            'total_leituras': total_leituras,
            'motores_online': motores_online,
            'alertas_criticos': alertas_criticos,
            'temperatura_media': round(temp_media, 1) if temp_media else 0,
            'potencia_total': round(float(potencia_total) / 1000, 1),
            'growth_rate': growth_rate,
            'system_health': round(system_health)
        },
        'chart_main': chart_data,
        'weekly_performance': weekly_performance,
        'gauge_value': round(system_health)
    }

    context = {
        'total_motores': total_motores,
        'total_sensores': total_sensores,
        'total_sensor_motor': total_sensor_motor,
        'ultimos_dados': ultimos_dados,
        'temperatura_media': round(temp_media, 1) if temp_media else 0,
        'alertas_criticos': alertas_criticos,
        'potencia_total': round(float(potencia_total) / 1000, 1),
        'growth_rate': growth_rate,
        'dashboard_json': json.dumps(dashboard_data, ensure_ascii=False)
    }
    
    return render(request, 'dashboard/index.html', context)