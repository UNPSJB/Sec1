from unittest.util import _MAX_LENGTH
from django.db import models

class Profesor(models.Model):
    dni: models.CharField(max_length=8)
    nombre: models.CharField(max_length=20)
    apellido: models.CharField(max_length=20)
    domicilio: models.CharField(max_length=50)
    telefono: models.CharField(max_length=20)
    especializacion: models.CharField(max_length=30)
    añosExperiencia: models.IntegerField(max_length=2)
    cbu: models.IntegerField(max_length=20)

    def __str__(self):
        return f'id={self.id}, dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}, domicilio={self.domicilio}, telefono={self.telefono}, especializacion={self.especializacion}, añosExperiencia={self.añosExperiencia}, cbu={self.cbu}'
# Create your models here.
