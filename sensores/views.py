from django.views import View
from django.shortcuts import render
from .factories import CrudFactory

class CrudView(View):
    model_name = None
    action = None

    def dispatch(self, request, *args, **kwargs):
        self.strategy = CrudFactory.get_strategy(self.model_name, self.action)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.strategy.handle_request(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.strategy.handle_request(request, *args, **kwargs)

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

class ListarSensorView(CrudView):
    model_name = 'sensor'
    action = 'list'

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
