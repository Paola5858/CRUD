from django.core.management.base import BaseCommand
from django.db.models import Avg, Min, Max, Count
from django.utils import timezone
from datetime import timedelta
from sensores.models import DadosSensor, DadosSensorAgregado


class Command(BaseCommand):
    help = 'Agrega dados históricos para otimizar performance'

    def add_arguments(self, parser):
        parser.add_argument('--periodo', type=str, default='DIA', 
                          choices=['HORA', 'DIA', 'SEMANA', 'MES'])
        parser.add_argument('--dias', type=int, default=30)

    def handle(self, *args, **options):
        periodo = options['periodo']
        dias_atras = options['dias']
        
        data_limite = timezone.now().date() - timedelta(days=dias_atras)
        
        dados = DadosSensor.objects.filter(
            data_hora__date__gte=data_limite
        ).values(
            'motor', 'sensor', 'data_hora__date'
        ).annotate(
            valor_min=Min('valor'),
            valor_max=Max('valor'),
            valor_avg=Avg('valor'),
            valor_count=Count('valor'),
            temp_min=Min('temperatura'),
            temp_max=Max('temperatura'),
            temp_avg=Avg('temperatura'),
            rpm_min=Min('rpm'),
            rpm_max=Max('rpm'),
            rpm_avg=Avg('rpm'),
        )
        
        agregados_criados = 0
        
        for dado in dados:
            agregado, created = DadosSensorAgregado.objects.get_or_create(
                motor_id=dado['motor'],
                sensor_id=dado['sensor'],
                data=dado['data_hora__date'],
                periodo=periodo,
                defaults={
                    'valor_min': dado['valor_min'],
                    'valor_max': dado['valor_max'],
                    'valor_avg': dado['valor_avg'],
                    'valor_count': dado['valor_count'],
                    'temp_min': dado['temp_min'],
                    'temp_max': dado['temp_max'],
                    'temp_avg': dado['temp_avg'],
                    'rpm_min': dado['rpm_min'],
                    'rpm_max': dado['rpm_max'],
                    'rpm_avg': dado['rpm_avg'],
                }
            )
            
            if created:
                agregados_criados += 1
        
        self.stdout.write(f'✅ {agregados_criados} agregações criadas')