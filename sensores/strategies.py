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
        return render(request, self.template_name, {'objects': objects})

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
