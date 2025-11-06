from django.db import models
from .models import Motor, Sensor, DadosSensor, SensorMotor

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

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

class SensorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Sensor)

class DadosSensorRepository(BaseRepository):
    def __init__(self):
        super().__init__(DadosSensor)

class SensorMotorRepository(BaseRepository):
    def __init__(self):
        super().__init__(SensorMotor)
