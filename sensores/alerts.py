"""
Sistema de alertas automáticos para MOTOSENSE.
"""

from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import AlertaConfig, EventoCritico, DadosSensor


class AlertManager:
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    def check_thresholds(self, dado_sensor):
        """Verifica se dados estão dentro dos limites configurados"""
        try:
            config = AlertaConfig.objects.get(
                motor=dado_sensor.motor,
                sensor=dado_sensor.sensor,
                ativo=True
            )
        except AlertaConfig.DoesNotExist:
            return
        
        alertas = []
        
        # Verificar valor
        if config.valor_min and dado_sensor.valor < config.valor_min:
            alertas.append({
                'tipo': 'VALOR_FORA',
                'descricao': f'Valor {dado_sensor.valor} abaixo do mínimo {config.valor_min}',
                'valor_atual': dado_sensor.valor,
                'valor_limite': config.valor_min
            })
        
        if config.valor_max and dado_sensor.valor > config.valor_max:
            alertas.append({
                'tipo': 'VALOR_FORA',
                'descricao': f'Valor {dado_sensor.valor} acima do máximo {config.valor_max}',
                'valor_atual': dado_sensor.valor,
                'valor_limite': config.valor_max
            })
        
        # Verificar temperatura
        if config.temp_max and dado_sensor.temperatura and dado_sensor.temperatura > config.temp_max:
            alertas.append({
                'tipo': 'TEMP_ALTA',
                'descricao': f'Temperatura {dado_sensor.temperatura}°C acima do limite {config.temp_max}°C',
                'valor_atual': dado_sensor.temperatura,
                'valor_limite': config.temp_max
            })
        
        # Verificar RPM
        if config.rpm_max and dado_sensor.rpm and dado_sensor.rpm > config.rpm_max:
            alertas.append({
                'tipo': 'RPM_ALTA',
                'descricao': f'RPM {dado_sensor.rpm} acima do limite {config.rpm_max}',
                'valor_atual': dado_sensor.rpm,
                'valor_limite': config.rpm_max
            })
        
        # Processar alertas
        for alerta in alertas:
            self.create_alert(dado_sensor, alerta, config)
    
    def create_alert(self, dado_sensor, alerta_data, config):
        """Cria evento crítico e envia notificações"""
        
        # Criar evento crítico
        evento = EventoCritico.objects.create(
            motor=dado_sensor.motor,
            sensor=dado_sensor.sensor,
            tipo=alerta_data['tipo'],
            valor_atual=alerta_data['valor_atual'],
            valor_limite=alerta_data['valor_limite'],
            descricao=alerta_data['descricao']
        )
        
        # Enviar via WebSocket
        self.send_websocket_alert(evento)
        
        # Enviar email se configurado
        if config.email_alerta:
            self.send_email_alert(evento, config.email_alerta)
    
    def send_websocket_alert(self, evento):
        """Envia alerta via WebSocket para dashboard"""
        if not self.channel_layer:
            return
        
        alert_data = {
            'tipo': evento.tipo,
            'titulo': self.get_alert_title(evento.tipo),
            'mensagem': evento.descricao,
            'motor': evento.motor.nome,
            'sensor': evento.sensor.tipo if evento.sensor else 'Sistema',
            'timestamp': evento.data_hora.isoformat()
        }
        
        async_to_sync(self.channel_layer.group_send)(
            'dashboard_updates',
            {
                'type': 'alert_update',
                'data': alert_data
            }
        )
    
    def send_email_alert(self, evento, email):
        """Envia alerta por email"""
        subject = f'[MOTOSENSE] Alerta: {self.get_alert_title(evento.tipo)}'
        message = f"""
        ALERTA CRÍTICO DETECTADO
        
        Motor: {evento.motor.nome}
        Sensor: {evento.sensor.tipo if evento.sensor else 'Sistema'}
        Tipo: {evento.tipo}
        Descrição: {evento.descricao}
        Data/Hora: {evento.data_hora.strftime('%d/%m/%Y %H:%M:%S')}
        
        Acesse o dashboard para mais detalhes.
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
    
    def get_alert_title(self, tipo):
        """Retorna título amigável para o tipo de alerta"""
        titles = {
            'TEMP_ALTA': 'Temperatura Alta',
            'RPM_ALTA': 'RPM Elevado',
            'VALOR_FORA': 'Valor Fora do Range',
            'DESCONECTADO': 'Sensor Desconectado',
            'RECONECTADO': 'Sensor Reconectado',
        }
        return titles.get(tipo, 'Alerta do Sistema')
    
    def check_sensor_connectivity(self):
        """Verifica conectividade dos sensores"""
        from django.utils import timezone
        from datetime import timedelta
        
        # Sensores que não enviam dados há mais de 5 minutos
        limite = timezone.now() - timedelta(minutes=5)
        
        # Buscar último dado de cada sensor
        sensores_ativos = DadosSensor.objects.values('motor', 'sensor').distinct()
        
        for sensor_info in sensores_ativos:
            ultimo_dado = DadosSensor.objects.filter(
                motor=sensor_info['motor'],
                sensor=sensor_info['sensor']
            ).order_by('-data_hora').first()
            
            if ultimo_dado and ultimo_dado.data_hora < limite:
                # Sensor desconectado
                evento, created = EventoCritico.objects.get_or_create(
                    motor_id=sensor_info['motor'],
                    sensor_id=sensor_info['sensor'],
                    tipo='DESCONECTADO',
                    resolvido=False,
                    defaults={
                        'descricao': f'Sensor não envia dados há mais de 5 minutos',
                        'valor_atual': None,
                        'valor_limite': None
                    }
                )
                
                if created:
                    self.send_websocket_alert(evento)


# Instância global do gerenciador de alertas
alert_manager = AlertManager()