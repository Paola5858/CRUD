from abc import ABC, abstractmethod
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import MotorService, SensorService, DadosSensorService
from .forms import MotorForm, SensorForm, DadosForm
import json

class CrudStrategy(ABC):
    def __init__(self, service, form_class, template_name):
        self.service = service
        self.form_class = form_class
        self.template_name = template_name

    @abstractmethod
    def handle_request(self, request, *args, **kwargs):
        pass

class ListStrategy(CrudStrategy):
    def handle_request(self, request, *args, **kwargs):
        objects = self.service.list_all()
        
        # Gerar dados JSON para JavaScript
        context = {'objects': objects}
        
        if 'motor' in self.template_name:
            import json
            import random
            from datetime import datetime
            
            motores_data = []
            for i, motor in enumerate(objects):
                # Gerar dados simulados realistas
                status_options = ['ONLINE', 'OFFLINE', 'MANUTENÇÃO', 'ERRO', 'STANDBY']
                tipo_motor = getattr(motor, 'tipo', 'INDUSTRIAL')
                
                motores_data.append({
                    'id': f'M-{str(i+1).zfill(3)}',
                    'name': motor.nome or f'Motor {i+1}',
                    'serial': f'{(motor.nome or "MOT")[:3].upper()}-2024-{str(i+1).zfill(2)}-X',
                    'type': tipo_motor,
                    'power': int(float(motor.potencia)) if motor.potencia else random.randint(800, 4000),
                    'temp': random.randint(55, 98),
                    'rpm': random.randint(1800, 5200),
                    'status': status_options[i % len(status_options)],
                    'lastSeen': f'Há {random.randint(1, 120)} min',
                    'created': motor.criado_em.strftime('%d/%m/%Y %H:%M') if hasattr(motor, 'criado_em') and motor.criado_em else datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'description': getattr(motor, 'descricao', f'Motor {tipo_motor.lower()} do sistema'),
                    'selected': False,
                    'expanded': False,
                    'critical': random.choice([True, False]) if i % 10 == 0 else False
                })
            
            context['motores_json'] = json.dumps(motores_data, ensure_ascii=False)
            
        elif 'sensor' in self.template_name:
            import json
            import random
            from datetime import datetime
            
            sensores_data = []
            for i, sensor in enumerate(objects):
                tipo_sensor = getattr(sensor, 'tipo', 'TEMPERATURA')
                
                sensores_data.append({
                    'id': f'S-{str(i+1).zfill(3)}',
                    'tipo': tipo_sensor,
                    'precisao': str(getattr(sensor, 'precisao', f'{random.uniform(0.1, 2.0):.1f}')),
                    'status': 'ATIVO' if i % 5 != 0 else 'INATIVO',
                    'valor_atual': random.randint(10, 100),
                    'unidade': 'ºC' if tipo_sensor == 'TEMPERATURA' else ('bar' if tipo_sensor == 'PRESSAO' else 'rpm'),
                    'created': sensor.criado_em.strftime('%d/%m/%Y %H:%M') if hasattr(sensor, 'criado_em') and sensor.criado_em else datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'selected': False
                })
            
            context['sensores_json'] = json.dumps(sensores_data, ensure_ascii=False)
            
        elif 'dados' in self.template_name:
            import json
            from datetime import datetime
            
            dados_data = []
            for i, dado in enumerate(objects):
                dados_data.append({
                    'id': dado.id if hasattr(dado, 'id') else i+1,
                    'sensor_tipo': getattr(dado.sensor, 'tipo', 'TEMPERATURA') if hasattr(dado, 'sensor') else 'TEMPERATURA',
                    'valor': float(dado.valor) if hasattr(dado, 'valor') and dado.valor else 0.0,
                    'data_hora': dado.data_hora.strftime('%d/%m/%Y %H:%M:%S') if hasattr(dado, 'data_hora') and dado.data_hora else datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    'selected': False
                })
            
            context['dados_json'] = json.dumps(dados_data, ensure_ascii=False)
        
        # Garantir que sempre há dados JSON, mesmo que vazio
        if 'motores_json' not in context:
            context['motores_json'] = '[]'
        if 'sensores_json' not in context:
            context['sensores_json'] = '[]'
        if 'dados_json' not in context:
            context['dados_json'] = '[]'
            
        return render(request, self.template_name, context)

class CreateStrategy(CrudStrategy):
    def handle_request(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Verificar se é requisição AJAX
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            form = self.form_class(request.POST)
            if form.is_valid():
                try:
                    obj = self.service.create(form.cleaned_data)
                    
                    if is_ajax:
                        return JsonResponse({
                            'success': True,
                            'message': 'Criado com sucesso!',
                            'data': {
                                'id': obj.id if hasattr(obj, 'id') else None,
                                'nome': getattr(obj, 'nome', str(obj))
                            }
                        })
                    else:
                        messages.success(request, 'Criado com sucesso!')
                        return redirect(request.path)
                        
                except Exception as e:
                    if is_ajax:
                        return JsonResponse({
                            'success': False,
                            'message': f'Erro ao criar: {str(e)}'
                        })
                    else:
                        messages.error(request, f'Erro ao criar: {str(e)}')
            else:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Dados inválidos',
                        'errors': form.errors
                    })
                    
        else:
            form = self.form_class()
            
        return render(request, self.template_name, {'form': form})

class UpdateStrategy(CrudStrategy):
    def handle_request(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.service.repository.model, id=id)
        
        if request.method == 'POST':
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            form = self.form_class(request.POST, instance=obj)
            if form.is_valid():
                try:
                    updated_obj = self.service.update(id, form.cleaned_data)
                    
                    if is_ajax:
                        return JsonResponse({
                            'success': True,
                            'message': 'Atualizado com sucesso!',
                            'data': {
                                'id': updated_obj.id if hasattr(updated_obj, 'id') else id,
                                'nome': getattr(updated_obj, 'nome', str(updated_obj))
                            }
                        })
                    else:
                        messages.success(request, 'Atualizado com sucesso!')
                        return redirect(request.path)
                        
                except Exception as e:
                    if is_ajax:
                        return JsonResponse({
                            'success': False,
                            'message': f'Erro ao atualizar: {str(e)}'
                        })
                    else:
                        messages.error(request, f'Erro ao atualizar: {str(e)}')
            else:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Dados inválidos',
                        'errors': form.errors
                    })
        else:
            form = self.form_class(instance=obj)
            
        return render(request, self.template_name, {'form': form, 'object': obj})

class DeleteStrategy(CrudStrategy):
    def handle_request(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.service.repository.model, id=id)
        
        if request.method == 'POST':
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            try:
                self.service.delete(id)
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Deletado com sucesso!'
                    })
                else:
                    messages.success(request, 'Deletado com sucesso!')
                    return redirect(request.path)
                    
            except Exception as e:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': f'Erro ao deletar: {str(e)}'
                    })
                else:
                    messages.error(request, f'Erro ao deletar: {str(e)}')
                    
        return render(request, self.template_name, {'object': obj})
