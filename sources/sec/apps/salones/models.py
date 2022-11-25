from unittest.util import _MAX_LENGTH
from django.db import models

from apps.personas.models import Persona
from apps.afiliados.models import Afiliado


class Salon(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    capacidad = models.PositiveIntegerField(max_length=4)
    monto = models.FloatField(max_length=9)
    encargado = models.ForeignKey(Persona, on_delete = models.CASCADE)
    afiliado = models.ManyToManyField(Afiliado, through = 'Alquiler')

    def alquilar(self, afiliado, senia, reserva, inicio):
        alquiler = Alquiler.agregarAlquiler(alquiler, self, senia, reserva, inicio, afiliado)
        self.save()

    def agregarSalon (self, nombre, direccion, capacidad, monto, encargado): 
        self.nombre = nombre 
        self.direccion = direccion 
        self.capacidad = capacidad 
        self.monto = monto 
        self.encargado = encargado
        self.save()

    def __str__(self):
        return f'{self.nombre} {self.direccion}'

class Servicio(models.Model): 
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=120)
    obligatorio = models.BooleanField(default = False)
    salon = models.ForeignKey(Salon, on_delete = models.CASCADE)

    #Revisar
    def agregarServicio (self, nombre, descripcion, obligatorio, salon): 
        self.nombre = nombre 
        self.descripcion = descripcion 
        self.obligatorio = obligatorio 
        self.salon = salon 
        self.save() 

    def __str__(self):
        return f'{self.nombre}'

class Alquiler (models.Model): 
    salon = models.ForeignKey(Salon, on_delete = models.CASCADE)
    afiliado = models.ForeignKey(Afiliado, on_delete = models.CASCADE)
    senia = models.FloatField(max_length = 8)
    reserva = models.DateField() 
    inicio = models.DateField( null = True, blank = True)
    monto = models.FloatField(max_length= 9)

    def agregarAlquiler (self, salon, senia, reserva, inicio, afiliado): 
        self.salon = salon 
        self.afiliado = afiliado 
        self.senia = senia 
        self.reserva = reserva 
        if (inicio): 
            self.inicio = inicio
        self.save()

class PagoAlquiler (models.Model): 
    TIPOPAGO = [(0, "debito"), (1, "credito"), (2, "efectivo")]
    alquiler = models.ForeignKey(Alquiler, on_delete = models.CASCADE)
    pago = models.DateField() 
    monto = models.FloatField(max_length = 9)
    formaPago = models.PositiveSmallIntegerField(choices = TIPOPAGO)
    
    #Revisar
    def agregarPago (self, alquiler, pago, monto, formaPago):
        self.alquiler = alquiler 
        self.pago = pago 
        self.monto = monto 
        self.formaPago = formaPago 
        self.save() 

