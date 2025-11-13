from django.test import TestCase, Client
from django.urls import reverse
from .models import Motor

class MotorModelTest(TestCase):
    def setUp(self):
        self.motor = Motor.objects.create(
            nome="Motor Teste",
            potencia=1500.00
        )
    
    def test_motor_creation(self):
        self.assertEqual(self.motor.nome, "Motor Teste")
        self.assertEqual(self.motor.potencia, 1500.00)
    
    def test_motor_str(self):
        self.assertEqual(str(self.motor), "Motor Teste")

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_dashboard_loads_successfully(self):
        """Test that the dashboard page loads with a 200 status code."""
        response = self.client.get(reverse('sensores:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sensores/dashboard.html')
        self.assertContains(response, 'Dashboard Principal')
    
    def test_dashboard_context_data(self):
        """Test that the dashboard view provides the correct context."""
        response = self.client.get(reverse('sensores:dashboard'))
        self.assertIn('total_motores', response.context)
        self.assertIn('total_sensores', response.context)
        self.assertIn('total_sensor_motor', response.context)
        self.assertIn('ultimos_dados', response.context)
        self.assertIn('ultimos_dados_json', response.context)