from unittest.util import _MAX_LENGTH
from django.db import models

class Persona(models.Model):
    dni = models.CharField(max_length=8)
    nombre = models.CharField(max_length= 30)
    apellido = models.CharField(max_length= 30)
    fechaNacimiento = models.DateTimeField()
    