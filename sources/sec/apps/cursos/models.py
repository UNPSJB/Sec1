from statistics import mode
from django.db import models

class Curso(models.Model):
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()
    cupo = models.IntegerField(2)
    modulos = models.IntegerField(2)
    descuento = models.IntegerField(2)
    precio = models.IntegerField(4)

    def __str__(self):
        return f'fechaDesde={self.fechaDesde}, fechaHasta={self.fechaHasta}, cupo={self.cupo}, modulos={self.modulos}, descuento={self.descuento}, precio={self.precio}'
