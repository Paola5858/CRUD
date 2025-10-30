from django.urls import path
from . import views

urlpatterns = [
    path('motores/', views.listar_motor, name='listar_motor'),
    path('sensores/', views.listar_sensor, name='listar_sensor'),
    path('motor-sensor/', views.listar_sensormotor, name='listar_sensormotor'),
    path('dados/', views.listar_dados, name='listar_dados'),
]
