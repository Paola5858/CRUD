"""
URLs para o app sensores com API REST.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views
from .api_views import MotorViewSet, SensorViewSet, DadosSensorViewSet, EventoCriticoViewSet, DashboardAPIView

app_name = 'sensores'

# API Router
router = DefaultRouter()
router.register('motores', MotorViewSet)
router.register('sensores', SensorViewSet)
router.register('dados', DadosSensorViewSet)
router.register('eventos', EventoCriticoViewSet)
router.register('dashboard', DashboardAPIView, basename='dashboard')

urlpatterns = [
    # Views tradicionais
    path('', views.ListarMotorView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Motor CRUD
    path('motor/', views.ListarMotorView.as_view(), name='listar_motor'),
    path('motor/criar/', views.CriarMotorView.as_view(), name='criar_motor'),
    path('motor/<int:pk>/editar/', views.AtualizarMotorView.as_view(), name='editar_motor'),
    path('motor/<int:pk>/deletar/', views.DeletarMotorView.as_view(), name='deletar_motor'),
    
    # Sensor CRUD
    path('sensor/', views.ListarSensorView.as_view(), name='listar_sensor'),
    path('sensor/criar/', views.CriarSensorView.as_view(), name='criar_sensor'),
    path('sensor/<int:pk>/editar/', views.AtualizarSensorView.as_view(), name='editar_sensor'),
    path('sensor/<int:pk>/deletar/', views.DeletarSensorView.as_view(), name='deletar_sensor'),
    
    # Dados CRUD
    path('dados/', views.ListarDadosView.as_view(), name='listar_dados'),
    path('dados/criar/', views.CriarDadosView.as_view(), name='criar_dados'),
    path('dados/<int:pk>/editar/', views.AtualizarDadosView.as_view(), name='editar_dados'),
    path('dados/<int:pk>/deletar/', views.DeletarDadosView.as_view(), name='deletar_dados'),
    
    # API REST
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='sensores:schema'), name='swagger-ui'),
]