from abc import ABC, abstractmethod
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .services import MotorService, SensorService, DadosSensorService
from .forms import MotorForm, SensorForm, DadosForm

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
        
        # Para motores, adicionar dados JSON para JavaScript
        context = {'objects': objects}
        if 'motor' in self.template_name:
            import json
            import random
            motores_data = []
            for i, motor in enumerate(objects):
                motores_data.append({
                    'id': f'M-{str(i+1).zfill(3)}',
                    'name': motor.nome,
                    'serial': f'{motor.nome[:3].upper()}-2024-{str(i+1).zfill(2)}-X',
                    'type': getattr(motor, 'tipo', 'INDUSTRIAL'),
                    'power': int(motor.potencia) if motor.potencia else random.randint(1000, 3000),
                    'temp': random.randint(70, 95),
                    'rpm': random.randint(2000, 4500),
                    'status': 'ONLINE' if i % 4 != 0 else 'OFFLINE',
                    'lastSeen': f'Há {random.randint(1, 60)} min',
                    'created': '01/11/2025 08:30',
                    'description': getattr(motor, 'descricao', 'Motor do sistema'),
                    'selected': False,
                    'expanded': False
                })
            context['motores_json'] = json.dumps(motores_data)
        
        return render(request, self.template_name, context)

class CreateStrategy(CrudStrategy):
    def handle_request(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                self.service.create(form.cleaned_data)
                messages.success(request, 'Criado com sucesso!')
                return redirect(request.path)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

class UpdateStrategy(CrudStrategy):
    def handle_request(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.service.repository.model, id=id)
        if request.method == 'POST':
            form = self.form_class(request.POST, instance=obj)
            if form.is_valid():
                self.service.update(id, form.cleaned_data)
                messages.success(request, 'Atualizado com sucesso!')
                return redirect(request.path)
        else:
            form = self.form_class(instance=obj)
        return render(request, self.template_name, {'form': form, 'object': obj})

class DeleteStrategy(CrudStrategy):
    def handle_request(self, request, id, *args, **kwargs):
        obj = get_object_or_404(self.service.repository.model, id=id)
        if request.method == 'POST':
            self.service.delete(id)
            messages.success(request, 'Deletado com sucesso!')
            return redirect(request.path)
        return render(request, self.template_name, {'object': obj})
