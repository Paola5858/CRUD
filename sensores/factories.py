from .strategies import ListStrategy, CreateStrategy, UpdateStrategy, DeleteStrategy
from .services import MotorService, SensorService, DadosSensorService
from .forms import MotorForm, SensorForm, DadosForm

class CrudFactory:
    @staticmethod
    def get_strategy(model_name, action):
        if model_name == 'motor':
            service = MotorService()
            form_class = MotorForm
            template_base = 'sensores/motor'
        elif model_name == 'sensor':
            service = SensorService()
            form_class = SensorForm
            template_base = 'sensores/sensor'
        elif model_name == 'dados':
            service = DadosSensorService()
            form_class = DadosForm
            template_base = 'sensores/dados'
        else:
            raise ValueError("Modelo inválido")

        if action == 'list':
            if model_name == 'dados':
                return ListStrategy(service, form_class, 'sensores/listar_dados.html')
            else:
                return ListStrategy(service, form_class, f'{template_base}_list.html')
        elif action == 'create':
            return CreateStrategy(service, form_class, f'{template_base}_form.html')
        elif action == 'update':
            return UpdateStrategy(service, form_class, f'{template_base}_form.html')
        elif action == 'delete':
            return DeleteStrategy(service, form_class, f'{template_base}_confirm_delete.html')
        else:
            raise ValueError("Ação inválida")
