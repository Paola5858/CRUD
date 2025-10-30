from django.contrib import admin
from .models import Motor, Sensor, SensorMotor, DadosSensor

@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Motor.
    """
    list_display = ('nome', 'potencia', 'criado_em')
    search_fields = ('nome',)

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Sensor.
    """
    list_display = ('tipo', 'precisao', 'criado_em')
    search_fields = ('tipo',)

@admin.register(SensorMotor)
class SensorMotorAdmin(admin.ModelAdmin):
    """
    Admin para o modelo SensorMotor.
    """
    list_display = ('motor', 'sensor')

@admin.register(DadosSensor)
class DadosSensorAdmin(admin.ModelAdmin):
    """
    Admin para o modelo DadosSensor.
    """
    list_display = ('motor', 'sensor', 'valor', 'data_hora')
    list_filter = ('motor', 'sensor', 'data_hora')
