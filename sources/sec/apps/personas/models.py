
import this
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    dni = models.CharField(max_length=8)
    nombre = models.CharField(max_length= 30)
    apellido = models.CharField(max_length= 30)
    fechaNacimiento = models.DateField()
    encargado = models.BooleanField() 
    usuario = models.OneToOneField(User, null = True, blank = True,  on_delete = models.CASCADE) 

    def __str__(self):
        return f'id={self.id}, dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}'


class Vinculo (models.Model): 
    TIPO = [(0, "Conyuge"), (1,"Hijo"), (2,"Tutor")] 
    tipoVinculo = models.PositiveSmallIntegerField(choices = TIPO)
    vinculante = models.ForeignKey(Persona, related_name = "vinculantes", on_delete = models.CASCADE) 
    vinculado = models.ForeignKey(Persona, related_name = "vinculados",  on_delete = models.CASCADE) 



class Rol(models.Model):
    TIPO = 0
    TIPOS = []
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    fechaDesde = models.DateTimeField(auto_now_add=True)
    fechaHasta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.persona} es {self.get_tipo_display()}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(Rol, self).save(*args, **kwargs)

    def related(self):
        return self.__class__ != Rol and self or getattr(self, self.get_tipo_display())

    @classmethod
    def register(cls, klass):
        cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))
