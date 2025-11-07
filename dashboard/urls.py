from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='index'),
    path('api/metrics/', views.dashboard_metrics_api, name='metrics_api'),
    path('api/motor-status/', views.motor_status_api, name='motor_status_api'),
    path('api/alerts/', views.alerts_api, name='alerts_api'),
]