"""
Views para gerenciamento de sensores e motores.

Este módulo contém todas as views responsáveis pelo CRUD
de motores, sensores e dados do sistema MOTOSENSE.

Autor: Paola Machado
Data: 2025-11-14
"""

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
    API endpoint que registra requisições e retorna mensagem de boas-vindas.
    
    Args:
        request (HttpRequest): Objeto de requisição Django
        
    Returns:
        JsonResponse: Mensagem de boas-vindas em JSON
        
    Example:
        >>> response = welcome_api(request)
        >>> response.status_code
        200
    """
    logger.info(f"Request received: {request.method} {request.path}")
    return JsonResponse({"message": "Welcome to the MOTOSENSE API Service!"})



class CrudView(LoginRequiredMixin, View):
    """
    View base para operações CRUD usando padrão Strategy.
    
    Esta classe implementa o padrão Strategy para delegar
    operações CRUD para estratégias específicas, garantindo
    código limpo e reutilizável.
    
    Attributes:
        model_name (str): Nome do modelo (motor, sensor, dados)
        action (str): Ação a ser executada (list, create, update, delete)
        
    Example:
        class ListarMotorView(CrudView):
            model_name = 'motor'
            action = 'list'
    """
    model_name = None
    action = None

    def dispatch(self, request, *args, **kwargs):
        """
        Intercepta requisições e configura estratégia apropriada.
        
        Args:
            request (HttpRequest): Requisição HTTP
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
            
        Returns:
            HttpResponse: Resposta da estratégia ou página de erro
            
        Raises:
            Http404: Se estratégia não for encontrada
        """
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
