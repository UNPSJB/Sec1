from unittest.util import _MAX_LENGTH
from django.db import models
import os
from django.conf import settings

from apps.personas.models import Persona
from apps.afiliados.models import Afiliado


class Salon(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    capacidad = models.PositiveIntegerField()
    monto = models.FloatField(max_length=9)
    encargado = models.ForeignKey(Persona, on_delete = models.CASCADE)
    imagen = models.ImageField(upload_to='static/img', null=True)
    #TODO: Asociar 2 imagenes mas
    descripcion = models.TextField(null=True, blank=False)
    afiliado = models.ManyToManyField(Afiliado, through = 'Alquiler')
    disponible = models.BooleanField(default=True)

    def alquilar(self, afiliado, senia, reserva, inicio,monto):
        alquiler = Alquiler.objects.create(alquiler, self, senia, reserva, inicio, afiliado, monto)
        self.save() 

    def cambiar_estado(self):
        self.disponible = not self.disponible
        self.save()

    def __str__(self):
        return f'{self.nombre}'
    
    
class Servicio(models.Model): 
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=120, null=True)
    precio = models.FloatField()
    obligatorio = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)
    salon = models.ForeignKey(Salon, on_delete= models.CASCADE)

    def cambiar_estado(self):
        self.disponible = not self.disponible
        self.save()


    def __str__(self):
        return f'{self.nombre}'

class Alquiler (models.Model): 
    salon = models.ForeignKey(Salon, on_delete = models.CASCADE)
    afiliado = models.ForeignKey(Afiliado, on_delete = models.CASCADE)
    senia = models.FloatField()
    reserva = models.DateField() 
    inicio = models.DateField()
    monto = models.FloatField()
    activo = models.BooleanField(default=True)
    
class PagoAlquiler(models.Model):
    alquiler = models.ForeignKey(Alquiler, on_delete = models.CASCADE)
    cuotas = models.IntegerField(default=1) #numero de cuotas totales/ seleccionables
    monto = models.DecimalField(max_digits=9,decimal_places=2)
    pago = models.DateField( null = True, blank = True)
    numero = models.IntegerField(default=1) #numero de cuota

# TODO: tener un solo modelo de pago para posteriormente filtrar alquileres inpagos
# TODO: hacer bajas logicas en lugar de deletes
# TODO: ver si es mejor una funcion para saber si un alquiler esta pagado