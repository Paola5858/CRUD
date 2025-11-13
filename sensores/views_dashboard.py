from django.shortcuts import render
from .models import Motor, Sensor, SensorMotor, DadosSensor

def dashboard(request):
    """Dashboard com QuerySet conforme especificação"""
    total_motores = Motor.objects.count()
    total_sensores = Sensor.objects.count()
    total_sensor_motor = SensorMotor.objects.count()
    ultimos_dados = DadosSensor.objects.select_related('motor', 'sensor').order_by('-data_hora')[:10]

    context = {
        'total_motores': total_motores,
        'total_sensores': total_sensores,
        'total_sensor_motor': total_sensor_motor,
        'ultimos_dados': ultimos_dados,
    }
    return render(request, 'sensores/dashboard.html', context)