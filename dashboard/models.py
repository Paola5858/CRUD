from django.db import models
from sensores.models import Motor, Sensor


class DashboardMetrics(models.Model):
    """Métricas pré-calculadas para performance"""
    data_calculo = models.DateField()
    total_sensores_ativos = models.IntegerField()
    total_motores_ativos = models.IntegerField()
    total_leituras_dia = models.IntegerField()
    media_valores = models.FloatField()
    
    class Meta:
        verbose_name = "Métrica do Dashboard"
        verbose_name_plural = "Métricas do Dashboard"


class AlertaSensor(models.Model):
    """Alertas do sistema"""
    TIPOS_ALERTA = [
        ('high_temp', 'Temperatura Alta'),
        ('low_pressure', 'Pressão Baixa'),
        ('offline', 'Sensor Offline'),
    ]
    
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    tipo_alerta = models.CharField(max_length=50, choices=TIPOS_ALERTA)
    valor_limite = models.FloatField()
    valor_atual = models.FloatField()
    criado_em = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Alerta de Sensor"
        verbose_name_plural = "Alertas de Sensores"