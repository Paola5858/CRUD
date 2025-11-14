"""
Serializers para API REST do MOTOSENSE.
"""

from rest_framework import serializers
from .models import Motor, Sensor, DadosSensor, SensorMotor, EventoCritico


class MotorSerializer(serializers.ModelSerializer):
    total_sensores = serializers.SerializerMethodField()
    ultimo_dado = serializers.SerializerMethodField()
    
    class Meta:
        model = Motor
        fields = ['id', 'nome', 'potencia', 'criado_em', 'ativo', 'total_sensores', 'ultimo_dado']
    
    def get_total_sensores(self, obj):
        return obj.sensormotor_set.count()
    
    def get_ultimo_dado(self, obj):
        ultimo = obj.dados.first()
        if ultimo:
            return {
                'valor': ultimo.valor,
                'temperatura': ultimo.temperatura,
                'rpm': ultimo.rpm,
                'data_hora': ultimo.data_hora
            }
        return None


class SensorSerializer(serializers.ModelSerializer):
    total_motores = serializers.SerializerMethodField()
    
    class Meta:
        model = Sensor
        fields = ['id', 'tipo', 'precisao', 'criado_em', 'ativo', 'total_motores']
    
    def get_total_motores(self, obj):
        return obj.sensormotor_set.count()


class DadosSensorSerializer(serializers.ModelSerializer):
    motor_nome = serializers.CharField(source='motor.nome', read_only=True)
    sensor_tipo = serializers.CharField(source='sensor.tipo', read_only=True)
    
    class Meta:
        model = DadosSensor
        fields = [
            'id', 'motor', 'sensor', 'motor_nome', 'sensor_tipo',
            'data_hora', 'valor', 'temperatura', 'rpm', 'pressao', 'fonte'
        ]


class DadosSensorCreateSerializer(serializers.ModelSerializer):
    """Serializer otimizado para criação via API"""
    
    class Meta:
        model = DadosSensor
        fields = ['motor', 'sensor', 'valor', 'temperatura', 'rpm', 'pressao']


class EventoCriticoSerializer(serializers.ModelSerializer):
    motor_nome = serializers.CharField(source='motor.nome', read_only=True)
    sensor_tipo = serializers.CharField(source='sensor.tipo', read_only=True)
    
    class Meta:
        model = EventoCritico
        fields = [
            'id', 'motor', 'sensor', 'motor_nome', 'sensor_tipo',
            'tipo', 'valor_atual', 'valor_limite', 'descricao',
            'resolvido', 'data_hora'
        ]


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer para estatísticas do dashboard"""
    total_motores = serializers.IntegerField()
    total_sensores = serializers.IntegerField()
    motores_online = serializers.IntegerField()
    dados_hoje = serializers.IntegerField()
    alertas_ativos = serializers.IntegerField()
    ultima_atualizacao = serializers.DateTimeField()