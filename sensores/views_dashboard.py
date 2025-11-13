from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Motor, Sensor, SensorMotor, DadosSensor
from .constants import DASHBOARD_RECENT_LIMIT

@login_required
def dashboard(request):
    """Dashboard com QuerySet conforme especificação"""
    import json
    from django.core.serializers.json import DjangoJSONEncoder

    total_motores = Motor.objects.count()
    total_sensores = Sensor.objects.count()
    total_sensor_motor = SensorMotor.objects.count()
    ultimos_dados = DadosSensor.objects.select_related("motor", "sensor").order_by(
        "-data_hora"
    )[:DASHBOARD_RECENT_LIMIT]

    # Serializar dados para JavaScript
    ultimos_dados_json = json.dumps([
        {
            'data_hora': dado.data_hora.isoformat() if dado.data_hora else None,
            'sensor_tipo': dado.sensor.tipo if dado.sensor else '',
            'motor_nome': dado.motor.nome if dado.motor else '',
            'valor': float(dado.valor) if dado.valor else 0
        }
        for dado in ultimos_dados
    ], cls=DjangoJSONEncoder)

    context = {
        "total_motores": total_motores,
        "total_sensores": total_sensores,
        "total_sensor_motor": total_sensor_motor,
        "ultimos_dados": ultimos_dados,
        "ultimos_dados_json": ultimos_dados_json,
        "user": request.user,  # Adicionar usuário ao contexto
    }
    return render(request, 'sensores/dashboard.html', context)
