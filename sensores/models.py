"""
Models otimizados para escalabilidade e performance.
"""

from django.db import models
from django.utils import timezone


class Motor(models.Model):
    nome = models.CharField(max_length=100, db_index=True)
    potencia = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['nome', 'ativo']),
            models.Index(fields=['-criado_em']),
        ]
    
    def __str__(self):
        return self.nome


class Sensor(models.Model):
    tipo = models.CharField(max_length=50, db_index=True)
    precisao = models.DecimalField(max_digits=5, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['tipo', 'ativo']),
        ]
    
    def __str__(self):
        return self.tipo


class SensorMotor(models.Model):
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('motor', 'sensor')
        indexes = [
            models.Index(fields=['motor', 'sensor']),
        ]


class DadosSensor(models.Model):
    """Tabela principal - será particionada por ano"""
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='dados')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='dados')
    data_hora = models.DateTimeField(auto_now_add=True, db_index=True)
    valor = models.FloatField(db_index=True)
    temperatura = models.FloatField(null=True, blank=True)
    rpm = models.IntegerField(null=True, blank=True)
    pressao = models.FloatField(null=True, blank=True)
    fonte = models.CharField(max_length=20, default='MANUAL', db_index=True)
    raw_json = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['-data_hora']),
            models.Index(fields=['motor', '-data_hora']),
            models.Index(fields=['sensor', '-data_hora']),
            models.Index(fields=['valor', '-data_hora']),
            models.Index(fields=['fonte', '-data_hora']),
        ]
    
    def __str__(self):
        return f"{self.motor.nome} - {self.sensor.tipo} - {self.valor}"


class DadosSensorAgregado(models.Model):
    """Tabela de agregação para dados históricos"""
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    data = models.DateField(db_index=True)
    periodo = models.CharField(max_length=10, choices=[
        ('HORA', 'Por Hora'),
        ('DIA', 'Por Dia'),
        ('SEMANA', 'Por Semana'),
        ('MES', 'Por Mês')
    ], db_index=True)
    
    # Agregações
    valor_min = models.FloatField()
    valor_max = models.FloatField()
    valor_avg = models.FloatField()
    valor_count = models.IntegerField()
    
    temp_min = models.FloatField(null=True)
    temp_max = models.FloatField(null=True)
    temp_avg = models.FloatField(null=True)
    
    rpm_min = models.IntegerField(null=True)
    rpm_max = models.IntegerField(null=True)
    rpm_avg = models.FloatField(null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('motor', 'sensor', 'data', 'periodo')
        indexes = [
            models.Index(fields=['data', 'periodo']),
            models.Index(fields=['motor', 'data']),
            models.Index(fields=['sensor', 'data']),
        ]


class AlertaConfig(models.Model):
    """Configuração de alertas por motor/sensor"""
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    
    # Thresholds
    valor_min = models.FloatField(null=True, blank=True)
    valor_max = models.FloatField(null=True, blank=True)
    temp_max = models.FloatField(null=True, blank=True)
    rpm_max = models.IntegerField(null=True, blank=True)
    
    # Configurações
    ativo = models.BooleanField(default=True)
    email_alerta = models.EmailField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('motor', 'sensor')


class EventoCritico(models.Model):
    """Log de eventos críticos e alertas"""
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, blank=True)
    
    tipo = models.CharField(max_length=20, choices=[
        ('TEMP_ALTA', 'Temperatura Alta'),
        ('RPM_ALTA', 'RPM Alta'),
        ('VALOR_FORA', 'Valor Fora do Range'),
        ('DESCONECTADO', 'Sensor Desconectado'),
        ('RECONECTADO', 'Sensor Reconectado'),
    ], db_index=True)
    
    valor_atual = models.FloatField(null=True)
    valor_limite = models.FloatField(null=True)
    descricao = models.TextField()
    resolvido = models.BooleanField(default=False, db_index=True)
    data_hora = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['-data_hora', 'resolvido']),
            models.Index(fields=['motor', '-data_hora']),
            models.Index(fields=['tipo', '-data_hora']),
        ]