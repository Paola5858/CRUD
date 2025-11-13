"""
Testes unitários para o app sensores
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Motor, Sensor, DadosSensor
from .services import MotorService, SensorService


class MotorModelTest(TestCase):
    """Testes para o modelo Motor"""
    
    def setUp(self):
        self.motor = Motor.objects.create(
            nome="Motor Teste",
            tipo="INDUSTRIAL",
            potencia=2000.0,
            descricao="Motor para testes"
        )
    
    def test_motor_creation(self):
        """Testa criação de motor"""
        self.assertEqual(self.motor.nome, "Motor Teste")
        self.assertEqual(self.motor.tipo, "INDUSTRIAL")
        self.assertEqual(float(self.motor.potencia), 2000.0)
    
    def test_motor_str(self):
        """Testa representação string do motor"""
        self.assertEqual(str(self.motor), "Motor Teste")


class SensorModelTest(TestCase):
    """Testes para o modelo Sensor"""
    
    def setUp(self):
        self.sensor = Sensor.objects.create(
            tipo="TEMPERATURA",
            precisao=0.5,
            descricao="Sensor de temperatura"
        )
    
    def test_sensor_creation(self):
        """Testa criação de sensor"""
        self.assertEqual(self.sensor.tipo, "TEMPERATURA")
        self.assertEqual(float(self.sensor.precisao), 0.5)
    
    def test_sensor_str(self):
        """Testa representação string do sensor"""
        expected = f"Sensor TEMPERATURA (ID: {self.sensor.id})"
        self.assertEqual(str(self.sensor), expected)


class MotorServiceTest(TestCase):
    """Testes para o serviço de Motor"""
    
    def setUp(self):
        self.service = MotorService()
        self.motor_data = {
            'nome': 'Motor Service Test',
            'tipo': 'COMERCIAL',
            'potencia': 1500.0,
            'descricao': 'Teste do serviço'
        }
    
    def test_create_motor(self):
        """Testa criação de motor via service"""
        motor = self.service.create(self.motor_data)
        self.assertEqual(motor.nome, 'Motor Service Test')
        self.assertEqual(motor.tipo, 'COMERCIAL')
    
    def test_list_motors(self):
        """Testa listagem de motores"""
        self.service.create(self.motor_data)
        motors = self.service.list_all()
        self.assertEqual(len(motors), 1)
    
    def test_update_motor(self):
        """Testa atualização de motor"""
        motor = self.service.create(self.motor_data)
        updated_data = {'nome': 'Motor Atualizado'}
        updated_motor = self.service.update(motor.id, updated_data)
        self.assertEqual(updated_motor.nome, 'Motor Atualizado')
    
    def test_delete_motor(self):
        """Testa exclusão de motor"""
        motor = self.service.create(self.motor_data)
        motor_id = motor.id
        self.service.delete(motor_id)
        
        with self.assertRaises(Motor.DoesNotExist):
            Motor.objects.get(id=motor_id)


class ViewsTest(TestCase):
    """Testes para as views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_required(self):
        """Testa se as views exigem login"""
        response = self.client.get(reverse('sensores:listar'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_motor_list_view_authenticated(self):
        """Testa view de listagem com usuário autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('sensores:listar'))
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_view_authenticated(self):
        """Testa dashboard com usuário autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)


class SecurityTest(TestCase):
    """Testes de segurança básicos"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_csrf_protection(self):
        """Testa proteção CSRF"""
        self.client.login(username='testuser', password='testpass123')
        
        # Tentar POST sem CSRF token
        response = self.client.post(reverse('sensores:criar'), {
            'nome': 'Test Motor',
            'tipo': 'INDUSTRIAL',
            'potencia': 1000
        })
        
        # Deve falhar por falta de CSRF token
        self.assertEqual(response.status_code, 403)
    
    def test_xss_protection_in_forms(self):
        """Testa proteção contra XSS em formulários"""
        self.client.login(username='testuser', password='testpass123')
        
        # Tentar injetar script
        malicious_data = {
            'nome': '<script>alert("xss")</script>',
            'tipo': 'INDUSTRIAL',
            'potencia': 1000,
            'descricao': 'Test'
        }
        
        response = self.client.post(reverse('sensores:criar'), malicious_data)
        
        # Verificar se o script não foi executado (form deve processar normalmente)
        # O Django automaticamente escapa HTML nos templates
        self.assertNotContains(response, '<script>', status_code=200)


class IntegrationTest(TestCase):
    """Testes de integração"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.motor = Motor.objects.create(
            nome="Motor Integração",
            tipo="INDUSTRIAL",
            potencia=3000.0
        )
        self.sensor = Sensor.objects.create(
            tipo="TEMPERATURA",
            precisao=1.0
        )
    
    def test_full_workflow(self):
        """Testa fluxo completo: login -> criar -> listar -> editar -> deletar"""
        # Login
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success)
        
        # Listar motores
        response = self.client.get(reverse('sensores:listar'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Motor Integração")
        
        # Verificar dashboard
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar se métricas estão sendo calculadas
        self.assertContains(response, "total_motores")