from tkinter.messagebox import NO, YES
from unittest.util import _MAX_LENGTH
from django.db import models
from unittest.util import _MAX_LENGTH


class Servicio(models.Model): 
    nombre = models.CharField(_MAX_LENGTH=20)
    descripcion = models.CharField(_MAX_LENGTH=120)
    obligatorio = models.BooleanField()

def __str__(self):
        return f'id={self.id}, nombre={self.nombre}, descripcion={self.descripcion}, obligatorio={self.obligatorio}'