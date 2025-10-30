from .repositories import MotorRepository, SensorRepository, DadosSensorRepository

class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def list_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, data):
        return self.repository.create(**data)

    def update(self, id, data):
        return self.repository.update(id, **data)

    def delete(self, id):
        self.repository.delete(id)

class MotorService(BaseService):
    def __init__(self):
        super().__init__(MotorRepository())

class SensorService(BaseService):
    def __init__(self):
        super().__init__(SensorRepository())

class DadosSensorService(BaseService):
    def __init__(self):
        super().__init__(DadosSensorRepository())
