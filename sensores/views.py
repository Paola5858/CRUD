from django.shortcuts import render

def listar_motor(request):
    return render(request, 'sensores/listar_motor.html')

def listar_sensor(request):
    return render(request, 'sensores/listar_sensor.html')

def listar_sensormotor(request):
    return render(request, 'sensores/listar_sensormotor.html')

def listar_dados(request):
    return render(request, 'sensores/listar_dados.html')
