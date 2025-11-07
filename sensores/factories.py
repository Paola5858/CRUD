from .strategies import ListStrategy, CreateStrategy, UpdateStrategy, DeleteStrategy
from .services import MotorService, SensorService, DadosSensorService, SensorMotorService
from .forms import MotorForm, SensorForm, DadosForm, SensorMotorForm
import logging

logger = logging.getLogger(__name__)

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
            template_base = 'sensores/dadossensor'
        elif model_name == 'sensormotor':
            service = SensorMotorService()
            form_class = SensorMotorForm
            template_base = 'sensores/sensormotor'
        else:
            logger.error(f"Modelo inválido: {model_name}")
            raise ValueError(f"Modelo inválido: {model_name}")

        if action == 'list':
            if model_name == 'motor':
                return ListStrategy(service, form_class, 'sensores/listar_motor.html')
            elif model_name == 'sensor':
                return ListStrategy(service, form_class, 'sensores/listar_sensor.html')
            elif model_name == 'dados':
                return ListStrategy(service, form_class, 'sensores/listar_dados.html')
            elif model_name == 'sensormotor':
                return ListStrategy(service, form_class, 'sensores/sensormotor_list.html')
            else:
                return ListStrategy(service, form_class, f'{template_base}_list.html')
        elif action == 'create':
            if model_name == 'dados':
                return CreateStrategy(service, form_class, 'sensores/dadossensor_form.html')
            elif model_name == 'sensormotor':
                return CreateStrategy(service, form_class, 'sensores/sensormotor_form.html')
            else:
                return CreateStrategy(service, form_class, f'{template_base}_form.html')
        elif action == 'update':
            if model_name == 'dados':
                return UpdateStrategy(service, form_class, 'sensores/dadossensor_form.html')
            elif model_name == 'sensormotor':
                return UpdateStrategy(service, form_class, 'sensores/sensormotor_form.html')
            else:
                return UpdateStrategy(service, form_class, f'{template_base}_form.html')
        elif action == 'delete':
            if model_name == 'dados':
                return DeleteStrategy(service, form_class, 'sensores/dadossensor_confirm_delete.html')
            elif model_name == 'sensormotor':
                return DeleteStrategy(service, form_class, 'sensores/sensormotor_confirm_delete.html')
            else:
                return DeleteStrategy(service, form_class, f'{template_base}_confirm_delete.html')
        else:
            logger.error(f"Ação inválida: {action}")
            raise ValueError(f"Ação inválida: {action}")
