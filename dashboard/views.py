from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from sensores.models import Motor, Sensor, DadosSensor


def dashboard_view(request):
    """View principal do dashboard"""
    return render(request, 'dashboard/index.html')


def dashboard_metrics_api(request):
    """API principal para métricas do dashboard"""
    
    # Dados para gráfico principal (últimos 12 meses)
    chart_data = []
    labels = []
    
    for i in range(12):
        date = timezone.now() - timedelta(days=30*i)
        count = DadosSensor.objects.filter(
            data_hora__month=date.month,
            data_hora__year=date.year
        ).count()
        chart_data.append(count)
        
        meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun',
                'jul', 'ago', 'set', 'out', 'nov', 'dez']
        labels.append(meses[date.month - 1])
    
    # Métricas gerais
    total_motores = Motor.objects.count()
    total_sensores = Sensor.objects.count()
    leituras_hoje = DadosSensor.objects.filter(
        data_hora__date=timezone.now().date()
    ).count()
    
    # Proporção por tipo de sensor
    sensor_types = Sensor.objects.values('tipo').annotate(
        count=Count('id')
    )
    
    return JsonResponse({
        'chart_main': {
            'labels': list(reversed(labels)),
            'data': list(reversed(chart_data))
        },
        'metrics': {
            'total_motores': total_motores,
            'total_sensores': total_sensores,
            'leituras_hoje': leituras_hoje,
            'crescimento': 47.8
        },
        'sensor_distribution': list(sensor_types),
        'status': 'success'
    })


def motor_status_api(request):
    """Status dos motores"""
    motores = Motor.objects.all()[:10]
    
    motor_status = []
    for motor in motores:
        ultima_leitura = DadosSensor.objects.filter(
            motor=motor
        ).order_by('-data_hora').first()
        
        is_online = False
        if ultima_leitura:
            diff = timezone.now() - ultima_leitura.data_hora
            is_online = diff.total_seconds() < 3600
        
        motor_status.append({
            'nome': motor.nome,
            'potencia': float(motor.potencia),
            'online': is_online,
            'ultima_atualizacao': ultima_leitura.data_hora.isoformat() if ultima_leitura else None
        })
    
    return JsonResponse({
        'motores': motor_status,
        'status': 'success'
    })