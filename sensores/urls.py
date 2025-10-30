from django.urls import path
from . import views

app_name = 'sensores'

urlpatterns = [
    path('motores/', views.ListarMotorView.as_view(), name='listar_motor'),
    path('motores/criar/', views.CriarMotorView.as_view(), name='criar_motor'),
    path('motores/<int:pk>/atualizar/',
         views.AtualizarMotorView.as_view(), name='atualizar_motor'),
    path('motores/<int:pk>/deletar/',
         views.DeletarMotorView.as_view(), name='deletar_motor'),
    path('sensores/', views.ListarSensorView.as_view(), name='listar_sensor'),
    path('sensores/criar/', views.CriarSensorView.as_view(), name='criar_sensor'),
    path('sensores/<int:pk>/atualizar/',
         views.AtualizarSensorView.as_view(), name='atualizar_sensor'),
    path('sensores/<int:pk>/deletar/',
         views.DeletarSensorView.as_view(), name='deletar_sensor'),
    path('dados/', views.ListarDadosView.as_view(), name='listar_dados'),
    path('dados/criar/', views.CriarDadosView.as_view(), name='criar_dados'),
    path('dados/<int:pk>/atualizar/',
         views.AtualizarDadosView.as_view(), name='atualizar_dados'),
    path('dados/<int:pk>/deletar/',
         views.DeletarDadosView.as_view(), name='deletar_dados'),
]
