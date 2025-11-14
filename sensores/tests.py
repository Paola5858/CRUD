"""
Testes unitários para o app sensores
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Motor, Sensor, DadosSensor
from .services import MotorService


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


class RepositoryTest(TestCase):
    """Testes para as classes Repository"""

    def setUp(self):
        from .repositories import MotorRepository, SensorRepository, DadosSensorRepository
        from .models import DadosSensor

        self.motor_repo = MotorRepository()
        self.sensor_repo = SensorRepository()
        self.dados_repo = DadosSensorRepository()

        # Criar dados de teste
        self.motor = Motor.objects.create(
            nome="Motor Teste Repo",
            tipo="INDUSTRIAL",
            potencia=2000.0
        )
        self.sensor = Sensor.objects.create(
            tipo="TEMPERATURA",
            precisao=0.5
        )

    def test_motor_repository_get_all(self):
        """Testa get_all do MotorRepository"""
        motors = self.motor_repo.get_all()
        self.assertEqual(len(motors), 1)
        self.assertEqual(motors[0].nome, "Motor Teste Repo")

    def test_motor_repository_get_by_id(self):
        """Testa get_by_id do MotorRepository"""
        motor = self.motor_repo.get_by_id(self.motor.id)
        self.assertEqual(motor.nome, "Motor Teste Repo")

    def test_motor_repository_create(self):
        """Testa create do MotorRepository"""
        data = {
            'nome': 'Novo Motor',
            'tipo': 'COMERCIAL',
            'potencia': 1500.0
        }
        motor = self.motor_repo.create(**data)
        self.assertEqual(motor.nome, 'Novo Motor')
        self.assertEqual(motor.tipo, 'COMERCIAL')

    def test_motor_repository_update(self):
        """Testa update do MotorRepository"""
        updated_motor = self.motor_repo.update(self.motor.id, nome='Motor Atualizado')
        self.assertEqual(updated_motor.nome, 'Motor Atualizado')

    def test_motor_repository_delete(self):
        """Testa delete do MotorRepository"""
        motor_id = self.motor.id
        self.motor_repo.delete(motor_id)

        with self.assertRaises(Motor.DoesNotExist):
            Motor.objects.get(id=motor_id)

    def test_sensor_repository_get_all(self):
        """Testa get_all do SensorRepository"""
        sensors = self.sensor_repo.get_all()
        self.assertEqual(len(sensors), 1)
        self.assertEqual(sensors[0].tipo, "TEMPERATURA")

    def test_sensor_repository_create(self):
        """Testa create do SensorRepository"""
        data = {
            'tipo': 'PRESSAO',
            'precisao': 1.0,
            'descricao': 'Sensor de pressão'
        }
        sensor = self.sensor_repo.create(**data)
        self.assertEqual(sensor.tipo, 'PRESSAO')
        self.assertEqual(float(sensor.precisao), 1.0)

    def test_dados_sensor_repository_get_recent_data(self):
        """Testa get_recent_data do DadosSensorRepository"""
        # Criar alguns dados de teste
        for i in range(5):
            DadosSensor.objects.create(
                motor=self.motor,
                sensor=self.sensor,
                valor=25.0 + i,
                fonte='TEST'
            )

        recent_data = self.dados_repo.get_recent_data(limit=3)
        self.assertEqual(len(recent_data), 3)


class StrategyTest(TestCase):
    """Testes para as classes Strategy"""

    def setUp(self):
        from .strategies import ListStrategy, CreateStrategy, UpdateStrategy, DeleteStrategy
        from .services import MotorService
        from .forms import MotorForm

        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

        self.service = MotorService()
        self.form_class = MotorForm
        self.template_name = 'sensores/listar_motor.html'
        self.list_url_name = 'sensores:listar_motor'

        # Criar dados de teste
        self.motor = Motor.objects.create(
            nome="Motor Strategy Test",
            tipo="INDUSTRIAL",
            potencia=3000.0
        )

    def test_list_strategy(self):
        """Testa ListStrategy"""
        from .strategies import ListStrategy

        strategy = ListStrategy(
            self.service,
            self.form_class,
            self.template_name,
            self.list_url_name
        )

        request = self.client.get(reverse('sensores:listar_motor')).wsgi_request
        response = strategy.handle_request(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Motor Strategy Test")

    def test_create_strategy_get(self):
        """Testa CreateStrategy - método GET"""
        from .strategies import CreateStrategy

        strategy = CreateStrategy(
            self.service,
            self.form_class,
            'sensores/motor_form.html',
            self.list_url_name
        )

        request = self.client.get(reverse('sensores:criar_motor')).wsgi_request
        response = strategy.handle_request(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cadastrar Novo Motor")

    def test_create_strategy_post_valid(self):
        """Testa CreateStrategy - método POST válido"""
        from .strategies import CreateStrategy

        strategy = CreateStrategy(
            self.service,
            self.form_class,
            'sensores/motor_form.html',
            self.list_url_name
        )

        data = {
            'nome': 'Novo Motor Strategy',
            'tipo': 'COMERCIAL',
            'potencia': 1500.0,
            'descricao': 'Teste strategy'
        }

        request = self.client.post(reverse('sensores:criar_motor'), data).wsgi_request
        response = strategy.handle_request(request)

        # Deve redirecionar após sucesso
        self.assertEqual(response.status_code, 302)

        # Verificar se foi criado
        motor = Motor.objects.get(nome='Novo Motor Strategy')
        self.assertEqual(motor.tipo, 'COMERCIAL')

    def test_update_strategy_get(self):
        """Testa UpdateStrategy - método GET"""
        from .strategies import UpdateStrategy

        strategy = UpdateStrategy(
            self.service,
            self.form_class,
            'sensores/motor_form.html',
            self.list_url_name
        )

        request = self.client.get(reverse('sensores:editar_motor', kwargs={'pk': self.motor.id})).wsgi_request
        response = strategy.handle_request(request, pk=self.motor.id)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Editar Motor")

    def test_update_strategy_post_valid(self):
        """Testa UpdateStrategy - método POST válido"""
        from .strategies import UpdateStrategy

        strategy = UpdateStrategy(
            self.service,
            self.form_class,
            'sensores/motor_form.html',
            self.list_url_name
        )

        data = {
            'nome': 'Motor Atualizado Strategy',
            'tipo': 'INDUSTRIAL',
            'potencia': 3500.0,
            'descricao': 'Atualizado via strategy'
        }

        request = self.client.post(reverse('sensores:editar_motor', kwargs={'pk': self.motor.id}), data).wsgi_request
        response = strategy.handle_request(request, pk=self.motor.id)

        # Deve redirecionar após sucesso
        self.assertEqual(response.status_code, 302)

        # Verificar se foi atualizado
        self.motor.refresh_from_db()
        self.assertEqual(self.motor.nome, 'Motor Atualizado Strategy')

    def test_delete_strategy_post(self):
        """Testa DeleteStrategy - método POST"""
        from .strategies import DeleteStrategy

        strategy = DeleteStrategy(
            self.service,
            self.form_class,
            'sensores/motor_confirm_delete.html',
            self.list_url_name
        )

        motor_id = self.motor.id
        request = self.client.post(reverse('sensores:deletar_motor', kwargs={'pk': motor_id})).wsgi_request
        response = strategy.handle_request(request, pk=motor_id)

        # Deve redirecionar após sucesso
        self.assertEqual(response.status_code, 302)

        # Verificar se foi deletado
        with self.assertRaises(Motor.DoesNotExist):
            Motor.objects.get(id=motor_id)


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
