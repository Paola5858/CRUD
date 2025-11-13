from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import EditPerfilForm

class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil.html'

class EditPerfilView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditPerfilForm
    template_name = 'edit_perfil.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user