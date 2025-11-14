# check_data.py - Verificar dados no banco
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from sensores.models import DadosSensor, Motor, Sensor

print("=" * 50)
print("VERIFICACAO DOS DADOS NO BANCO")
print("=" * 50)

print(f"Total de Motores: {Motor.objects.count()}")
print(f"Total de Sensores: {Sensor.objects.count()}")
print(f"Total de Dados: {DadosSensor.objects.count()}")

print("\nMotores cadastrados:")
for motor in Motor.objects.all():
    print(f"- ID: {motor.id}, Nome: {motor.nome}, Potencia: {motor.potencia}")

print("\nSensores cadastrados:")
for sensor in Sensor.objects.all():
    print(f"- ID: {sensor.id}, Tipo: {sensor.tipo}, Precisao: {sensor.precisao}")

print("\nUltimos 5 dados:")
for dado in DadosSensor.objects.all().order_by('-data_hora')[:5]:
    print(f"- ID: {dado.id}, Motor: {dado.motor.nome}, Sensor: {dado.sensor.tipo}")
    print(f"  Valor: {dado.valor}, Fonte: {dado.fonte}, Data: {dado.data_hora}")

print("=" * 50)