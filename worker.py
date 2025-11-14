# worker.py - Worker MQTT com credenciais CloudAMQP
import django
import os
import sys
import json
import time
import logging
import paho.mqtt.client as mqtt
from datetime import datetime

# ========== CONFIGURAR DJANGO ==========
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from sensores.models import DadosSensor, Motor, Sensor

# ========== CONFIGURAR LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/mqtt_worker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========== CONFIGURAÇÕES MQTT (CLOUDAMQP) ==========
BROKER = os.getenv('MQTT_BROKER')
PORT = int(os.getenv('MQTT_PORT', 1883))
TOPIC = os.getenv('MQTT_TOPIC', 'dadosSensor')
USERNAME = os.getenv('MQTT_USERNAME')
PASSWORD = os.getenv('MQTT_PASSWORD')

# Validar credenciais obrigatórias
if not BROKER or not USERNAME or not PASSWORD:
    raise ValueError("Credenciais MQTT obrigatórias não encontradas. Configure MQTT_BROKER, MQTT_USERNAME e MQTT_PASSWORD no arquivo .env")
CLIENT_ID = "motosense_worker_001"  # ID único - MANTER APENAS 1 WORKER RODANDO!

# ========== VARIÁVEIS GLOBAIS ==========
reconnect_count = 0
max_reconnect_attempts = 10

# ========== CALLBACK: CONEXÃO ==========
def on_connect(client, userdata, flags, rc):
    global reconnect_count
    
    if rc == 0:
        logger.info("=" * 60)
        logger.info("CONECTADO AO BROKER CLOUDAMQP!")
        logger.info(f"Broker: {BROKER}")
        logger.info(f"Topico: {TOPIC}")
        logger.info("=" * 60)
        
        client.subscribe(TOPIC)
        logger.info(f"Escutando mensagens no topico '{TOPIC}'...")
        reconnect_count = 0
        
    else:
        error_messages = {
            1: "Protocolo incorreto",
            2: "Client ID rejeitado",
            3: "Servidor indisponível",
            4: "Usuário/senha inválidos",
            5: "Não autorizado"
        }
        logger.error(f"FALHA NA CONEXAO! Codigo: {rc} - {error_messages.get(rc, 'Erro desconhecido')}")

# ========== CALLBACK: DESCONEXÃO ==========
def on_disconnect(client, userdata, rc):
    global reconnect_count
    
    if rc != 0:
        logger.warning(f"⚠️ DESCONECTADO INESPERADAMENTE! Código: {rc}")
        
        if reconnect_count < max_reconnect_attempts:
            reconnect_count += 1
            wait_time = min(2 ** reconnect_count, 60)  # Exponential backoff
            logger.info(f"🔄 Tentativa {reconnect_count}/{max_reconnect_attempts} em {wait_time}s...")
            time.sleep(wait_time)
        else:
            logger.error("❌ Número máximo de tentativas de reconexão atingido!")

# ========== CALLBACK: MENSAGEM RECEBIDA ==========
def on_message(client, userdata, msg):
    try:
        # Decodificar payload
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info("=" * 60)
        logger.info(f"MENSAGEM RECEBIDA [{timestamp}]")
        logger.info(f"Topico: {topic}")
        logger.info(f"Payload: {payload}")
        logger.info("=" * 60)

        # Parser JSON
        data = json.loads(payload)
        
        # Aceitar ambos os formatos (motor_id ou motorid)
        motor_id = data.get('motor_id') or data.get('motorid')
        sensor_id = data.get('sensor_id') or data.get('sensorid')
        valor = data.get('valor')
        
        if not motor_id or not sensor_id or not valor:
            logger.error(f"JSON INVALIDO! Faltam campos obrigatorios")
            logger.error(f"   Recebido: {data}")
            logger.error(f"   Esperado: motor_id/motorid, sensor_id/sensorid, valor")
            return

        # Buscar Motor e Sensor
        try:
            motor = Motor.objects.get(id=motor_id)
            logger.info(f"Motor encontrado: {motor.nome} (ID: {motor.id})")
        except Motor.DoesNotExist:
            logger.error(f"MOTOR NAO ENCONTRADO! ID: {motor_id}")
            logger.error(f"   Cadastre o motor no Django Admin primeiro!")
            return

        try:
            sensor = Sensor.objects.get(id=sensor_id)
            logger.info(f"Sensor encontrado: {sensor.tipo} (ID: {sensor.id})")
        except Sensor.DoesNotExist:
            logger.error(f"SENSOR NAO ENCONTRADO! ID: {sensor_id}")
            logger.error(f"   Cadastre o sensor no Django Admin primeiro!")
            return

        # Criar registro no banco
        dado = DadosSensor.objects.create(
            motor=motor,
            sensor=sensor,
            valor=valor,
            temperatura=data.get('temperatura'),
            rpm=data.get('rpm'),
            pressao=data.get('pressao'),
            fonte='MQTT',
            raw_json=data
        )
        
        # Enviar via WebSocket para dashboard em tempo real
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    'dashboard_updates',
                    {
                        'type': 'sensor_update',
                        'data': {
                            'motor_nome': motor.nome,
                            'sensor_tipo': sensor.tipo,
                            'valor': valor,
                            'temperatura': data.get('temperatura'),
                            'rpm': data.get('rpm'),
                            'timestamp': dado.data_hora.isoformat()
                        }
                    }
                )
        except Exception as e:
            logger.warning(f"Erro ao enviar WebSocket: {e}")
        
        # Verificar alertas
        try:
            from sensores.alerts import alert_manager
            alert_manager.check_thresholds(dado)
        except Exception as e:
            logger.warning(f"Erro ao verificar alertas: {e}")

        logger.info("=" * 60)
        logger.info("DADOS SALVOS COM SUCESSO!")
        logger.info(f"   ID do Registro: {dado.id}")
        logger.info(f"   Motor: {motor.nome}")
        logger.info(f"   Sensor: {sensor.tipo}")
        logger.info(f"   Valor: {valor}")
        logger.info(f"   Timestamp: {dado.data_hora}")
        logger.info("=" * 60)

    except json.JSONDecodeError as e:
        logger.error(f"❌ ERRO AO DECODIFICAR JSON: {e}")
        logger.error(f"   Payload recebido: {payload}")
    except Exception as e:
        logger.error(f"❌ ERRO AO PROCESSAR MENSAGEM: {e}", exc_info=True)

# ========== CALLBACK: LOG DE EVENTOS ==========
def on_log(client, userdata, level, buf):
    logger.debug(f"LOG MQTT: {buf}")

# ========== INICIALIZAR WORKER ==========
def start_worker():
    logger.info("\n" + "=" * 60)
    logger.info("INICIANDO WORKER MQTT MOTOSENSE")
    logger.info("=" * 60)
    logger.info(f"Broker: {BROKER}:{PORT}")
    logger.info(f"Usuario: {USERNAME}")
    logger.info(f"Topico: {TOPIC}")
    logger.info("AVISO: CloudAMQP gratuito - manter apenas 1 worker ativo!")
    logger.info("=" * 60 + "\n")
    
    # Criar diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # Configurar cliente MQTT
    client = mqtt.Client(
        client_id=CLIENT_ID,
        clean_session=True,
        protocol=mqtt.MQTTv311
    )
    
    # Configurar autenticação CloudAMQP
    client.username_pw_set(USERNAME, PASSWORD)
    
    # Registrar callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_log = on_log
    
    try:
        logger.info(f"Conectando ao broker CloudAMQP...")
        client.connect(BROKER, PORT, 60)
        
        logger.info("Worker rodando. Aguardando mensagens MQTT...")
        logger.info("   (Pressione Ctrl+C para parar)\n")
        
        # Loop infinito
        client.loop_forever()
        
    except KeyboardInterrupt:
        logger.info("\n⏹️ Worker interrompido pelo usuário.")
        client.disconnect()
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ ERRO FATAL: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    start_worker()