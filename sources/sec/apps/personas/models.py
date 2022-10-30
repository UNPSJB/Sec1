
import this
from unittest.util import _MAX_LENGTH
from django.db import models

class Persona(models.Model):
    dni = models.CharField(max_length=8)
    nombre = models.CharField(max_length= 30)
    apellido = models.CharField(max_length= 30)
    fechaNacimiento = models.DateField()
    encargado = models.BooleanField() 
    tipoRelacion = models.ManyToManyField( 'self' , null = True, through = 'Relacion', related_name = 'relacionados')

    def __str__(self):
        return f'id={self.id}, dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}'


class Relacion (models.Model): 
    TIPO = [] 
    tipoParentesco = models.PositiveSmallIntegerField(choices = TIPO)
    persona = models.ForeignKey(Persona, on_delete = models.CASCADE) 
    relacionado = models.ForeignKey(Persona, on_delete = models.CASCADE) 



class Rol(models.Model):
    TIPO = 0
    TIPOS = []
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    desde = models.DateTimeField(auto_now_add=True)
    hasta = models.DateTimeField(null=True, blank=True)

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
