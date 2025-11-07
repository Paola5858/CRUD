from django.db import models
from .models import Motor, Sensor, DadosSensor, SensorMotor

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()
    
    def get_all_optimized(self):
        """Override in subclasses for optimized queries"""
        return self.get_all()

    def get_by_id(self, id):
        return self.model.objects.get(id=id)

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, id, **kwargs):
        obj = self.get_by_id(id)
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        obj.delete()

class MotorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Motor)
    
    def get_all_optimized(self):
        """Otimizado para evitar N+1 queries com sensores"""
        return self.model.objects.prefetch_related(
            'sensormotor_set__sensor'
        ).all()

class SensorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Sensor)
    
    def get_all_optimized(self):
        """Otimizado para evitar N+1 queries com motores"""
        return self.model.objects.prefetch_related(
            'sensormotor_set__motor'
        ).all()

class DadosSensorRepository(BaseRepository):
    def __init__(self):
        super().__init__(DadosSensor)
    
    def get_all_optimized(self):
        """Otimizado para evitar N+1 queries com sensor"""
        return self.model.objects.select_related('sensor').all()
    
    def get_recent_data(self, limit=1000):
        """Buscar dados recentes com otimização"""
        return self.model.objects.select_related('sensor').order_by('-data_hora')[:limit]

class SensorMotorRepository(BaseRepository):
    def __init__(self):
        super().__init__(SensorMotor)
    
    def get_all_optimized(self):
        """Otimizado para evitar N+1 queries com motor e sensor"""
        return self.model.objects.select_related('motor', 'sensor').all()
