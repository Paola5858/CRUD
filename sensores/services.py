from .repositories import MotorRepository, SensorRepository, DadosSensorRepository, SensorMotorRepository

class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def list_all(self):
        return self.repository.get_all_optimized()

    def get_by_id(self, obj_id):
        return self.repository.get_by_id(obj_id)

    def create(self, data):
        return self.repository.create(**data)

    def update(self, obj_id, data):
        return self.repository.update(obj_id, **data)

    def delete(self, obj_id):
        self.repository.delete(obj_id)

class MotorService(BaseService):
    def __init__(self):
        super().__init__(MotorRepository())

class SensorService(BaseService):
    def __init__(self):
        super().__init__(SensorRepository())

class DadosSensorService(BaseService):
    def __init__(self):
        super().__init__(DadosSensorRepository())
    
    def get_recent_data(self, limit=1000):
        """Buscar dados recentes otimizado"""
        return self.repository.get_recent_data(limit)

class SensorMotorService(BaseService):
    def __init__(self):
        super().__init__(SensorMotorRepository())
