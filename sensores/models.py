from django.db import models

class Motor(models.Model):
    """
    Modelo para representar um motor.
    """
    nome = models.CharField(max_length=100, help_text="Nome do motor")
    potencia = models.DecimalField(max_digits=10, decimal_places=2, help_text="Potência do motor em watts")
    criado_em = models.DateTimeField(auto_now_add=True, help_text="Data de criação")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Motor"
        verbose_name_plural = "Motores"

class Sensor(models.Model):
    """
    Modelo para representar um sensor.
    """
    tipo = models.CharField(max_length=50, help_text="Tipo do sensor (ex: temperatura, pressão)")
    precisao = models.DecimalField(max_digits=5, decimal_places=2, help_text="Precisão do sensor")
    criado_em = models.DateTimeField(auto_now_add=True, help_text="Data de criação")

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"

class SensorMotor(models.Model):
    """
    Modelo para associar sensores a motores.
    """
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, help_text="Motor associado")
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, help_text="Sensor associado")

    def __str__(self):
        return f"{self.motor.nome} - {self.sensor.tipo}"

    class Meta:
        verbose_name = "Sensor do Motor"
        verbose_name_plural = "Sensores dos Motores"

class DadosSensor(models.Model):
    """
    Modelo para armazenar dados coletados pelos sensores.
    """
    data_hora = models.DateTimeField(auto_now=True, help_text="Data e hora da coleta")
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, help_text="Motor relacionado")
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, help_text="Sensor que coletou o dado")
    valor = models.FloatField(help_text="Valor coletado pelo sensor")

    def __str__(self):
        return f"{self.motor.nome} - {self.sensor.tipo}: {self.valor}"

    class Meta:
        verbose_name = "Dado do Sensor"
        verbose_name_plural = "Dados dos Sensores"
