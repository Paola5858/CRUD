from django.views import View
from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
import json
from .factories import CrudFactory
from .models import Motor, Sensor, SensorMotor, DadosSensor

logger = logging.getLogger(__name__)

def welcome_api(request):
    """
    API endpoint that logs requests and returns a welcome message.
    """
    logger.info(f"Request received: {request.method} {request.path}")
    return JsonResponse({"message": "Welcome to the MOTOSENSE API Service!"})



class CrudView(LoginRequiredMixin, View):
    model_name = None
    action = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.strategy = CrudFactory.get_strategy(self.model_name, self.action)
            return super().dispatch(request, *args, **kwargs)
        except ValueError as e:
            logger.error(f"Erro na factory: {e}")
            raise Http404("Recurso não encontrado")
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            messages.error(request, "Ocorreu um erro inesperado. Tente novamente.")
            return render(request, '500.html', status=500)

    def get(self, request, *args, **kwargs):
        try:
            return self.strategy.handle_request(request, *args, **kwargs)
        except Http404:
            raise
        except Exception as e:
            logger.error(f"Erro no GET: {e}")
            messages.error(request, "Erro ao carregar a página.")
            return render(request, '500.html', status=500)

    def post(self, request, *args, **kwargs):
        try:
            return self.strategy.handle_request(request, *args, **kwargs)
        except IntegrityError as e:
            logger.error(f"Erro de integridade: {e}")
            messages.error(request, "Erro de dados. Verifique as informações e tente novamente.")
            return self.get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro no POST: {e}")
            messages.error(request, "Erro ao processar a solicitação.")
            return self.get(request, *args, **kwargs)

class ListarMotorView(CrudView):
    model_name = 'motor'
    action = 'list'

class CriarMotorView(CrudView):
    model_name = 'motor'
    action = 'create'

class AtualizarMotorView(CrudView):
    model_name = 'motor'
    action = 'update'

class DeletarMotorView(CrudView):
    model_name = 'motor'
    action = 'delete'

class ListarSensorView(LoginRequiredMixin, View):
    def get(self, request):
        sensores = Sensor.objects.all()
        return render(request, 'sensores/listar_sensor.html', {'objects': sensores})

class CriarSensorView(CrudView):
    model_name = 'sensor'
    action = 'create'

class AtualizarSensorView(CrudView):
    model_name = 'sensor'
    action = 'update'

class DeletarSensorView(CrudView):
    model_name = 'sensor'
    action = 'delete'

class ListarDadosView(CrudView):
    model_name = 'dados'
    action = 'list'

class CriarDadosView(CrudView):
    model_name = 'dados'
    action = 'create'

class AtualizarDadosView(CrudView):
    model_name = 'dados'
    action = 'update'

class DeletarDadosView(CrudView):
    model_name = 'dados'
    action = 'delete'

class ListarSensorMotorView(CrudView):
    model_name = 'sensormotor'
    action = 'list'

class CriarSensorMotorView(CrudView):
    model_name = 'sensormotor'
    action = 'create'

class AtualizarSensorMotorView(CrudView):
    model_name = 'sensormotor'
    action = 'update'

class DeletarSensorMotorView(CrudView):
    model_name = 'sensormotor'
    action = 'delete'
