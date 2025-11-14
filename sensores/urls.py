from django.urls import path
from django.shortcuts import redirect
from django.views.generic import RedirectView
from . import views
from dashboard.views import dashboard_view

app_name = 'sensores'

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="sensores:dashboard", permanent=False),
        name="home",
    ),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("welcome/", views.welcome_api, name="welcome_api"),
    path("motores/", views.ListarMotorView.as_view(), name="listar_motor"),
    path("motores/criar/", views.CriarMotorView.as_view(), name="criar_motor"),
    path(
        "motores/<int:pk>/atualizar/",
        views.AtualizarMotorView.as_view(),
        name="atualizar_motor",
    ),
    path(
        "motores/<int:pk>/deletar/",
        views.DeletarMotorView.as_view(),
        name="deletar_motor",
    ),
    path("sensor/", views.ListarSensorView.as_view(), name="listar_sensor"),
    path("sensor/criar/", views.CriarSensorView.as_view(), name="criar_sensor"),
    path(
        "sensor/<int:pk>/atualizar/",
        views.AtualizarSensorView.as_view(),
        name="atualizar_sensor",
    ),
    path(
        "sensor/<int:pk>/deletar/",
        views.DeletarSensorView.as_view(),
        name="deletar_sensor",
    ),
    path("dados/", views.ListarDadosView.as_view(), name="listar_dados"),
    path("dados/criar/", views.CriarDadosView.as_view(), name="criar_dados"),
    path(
        "dados/<int:pk>/atualizar/",
        views.AtualizarDadosView.as_view(),
        name="atualizar_dados",
    ),
    path(
        "dados/<int:pk>/deletar/",
        views.DeletarDadosView.as_view(),
        name="deletar_dados",
    ),
    path(
        "sensor-motor/",
        views.ListarSensorMotorView.as_view(),
        name="listar_sensormotor",
    ),
    path(
        "sensor-motor/criar/",
        views.CriarSensorMotorView.as_view(),
        name="criar_sensormotor",
    ),
    path(
        "sensor-motor/<int:pk>/atualizar/",
        views.AtualizarSensorMotorView.as_view(),
        name="atualizar_sensormotor",
    ),
    path(
        "sensor-motor/<int:pk>/deletar/",
        views.DeletarSensorMotorView.as_view(),
        name="deletar_sensormotor",
    ),
]
