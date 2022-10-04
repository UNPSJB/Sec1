from unittest.util import _MAX_LENGTH
from django.db import models
from sources.sec.apps.personas.models import Aula
from sources.sec.apps.personas.models import Curso
from sources.sec.apps.personas.models import Profesor


class Dictado(models.Model): 
    aula = models.ManyToManyField(Aula)
    cursos = models.ManyToOneRel(Curso)
    profesores = models.ManyToManyField(Profesor) 
    costo = models.FloatField(_MAX_LENGTH=10)
    fechaInicio = models.DateField()
    fechaFin = models.DateField() 


def __str__(self):
    return f'id={self.id}, aula={self.aula}, cursos={self.cursos}, profesores={self.profesores}, costo={self.costo}, fechaInicio={self.fechaInicio}, fechaFin = {self.fechaFin}'
