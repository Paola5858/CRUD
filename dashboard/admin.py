from django.contrib import admin
from .models import DashboardMetrics, AlertaSensor


@admin.register(DashboardMetrics)
class DashboardMetricsAdmin(admin.ModelAdmin):
    list_display = ['data_calculo', 'total_sensores_ativos', 'total_motores_ativos', 'total_leituras_dia']
    list_filter = ['data_calculo']
    ordering = ['-data_calculo']


@admin.register(AlertaSensor)
class AlertaSensorAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'motor', 'tipo_alerta', 'valor_atual', 'criado_em', 'resolvido']
    list_filter = ['tipo_alerta', 'resolvido', 'criado_em']
    search_fields = ['sensor__tipo', 'motor__nome']
    ordering = ['-criado_em']