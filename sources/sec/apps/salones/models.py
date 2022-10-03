from unittest.util import _MAX_LENGTH
from django.db import models

from sources.sec.apps.personas.models import Persona

class Salon(models.Model):
    nombre: models.CharField(max_length=30)
    direccion: models.CharField(max_length=30)
    capacidad: models.PositiveIntegerField(max_length=3)
    montoSalon: models.FloatField(max_length=5)
    encargado: models.ForeignKey(Persona)

    def __str__(self):
        return f'id={self.id}, nombre={self.nombre}, direccion={self.direccion}, capacidad={self.capacidad}, montoSalon={self.montoSalon}, encargado={self.encargado}'
# Create your models here.
