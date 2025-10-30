from django import forms
from .models import Motor, Sensor, DadosSensor

class MotorForm(forms.ModelForm):
    """
    Formulário para o modelo Motor.
    """
    class Meta:
        model = Motor
        fields = ['nome', 'potencia']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do motor'}),
            'potencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Potência em watts'}),
        }

class SensorForm(forms.ModelForm):
    """
    Formulário para o modelo Sensor.
    """
    class Meta:
        model = Sensor
        fields = ['tipo', 'precisao']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo do sensor'}),
            'precisao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precisão'}),
        }

class DadosForm(forms.ModelForm):
    """
    Formulário para o modelo DadosSensor.
    """
    class Meta:
        model = DadosSensor
        fields = ['motor', 'sensor', 'valor']
        widgets = {
            'motor': forms.Select(attrs={'class': 'form-control'}),
            'sensor': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor coletado'}),
        }
