from django.db import models
from unittest.util import _MAX_LENGTH


class Aula(models.model): 
    nroAula = models.PositiveIntegerField(_MAX_LENGTH=30)
    capacidad = models.PositiveIntegerField(_MAX_LENGTH=2)

def __str__ (self): 
    return f'id={self.id}, nroAula={self.nroAula}, capacidad={self.capacidad}'


