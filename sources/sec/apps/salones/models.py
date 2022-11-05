from unittest.util import _MAX_LENGTH
from django.db import models

from apps.personas.models import Persona
from apps.afiliados.models import Afiliado

class Salon(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    capacidad = models.PositiveIntegerField(max_length=3)
    montoSalon = models.FloatField(max_length=5)
    encargado = models.ForeignKey(Persona, on_delete = models.CASCADE)
    afiliado = models.ManyToManyField(Afiliado, through = 'Alquiler')


    def agregarSalon (self, nombre, direccion, capacidad, monto, encargado, afiliado): 
        self.nombre = nombre 
        self.direccion = direccion 
        self.capacidad = capacidad 
        self.monto = monto 
        self.encargado = encargado
        self.afiliado = afiliado
        self.save()

    def __str__(self):
        return f'id={self.id}, nombre={self.nombre}, direccion={self.direccion}, capacidad={self.capacidad}, montoSalon={self.montoSalon}, encargado={self.encargado}'

class Servicio(models.Model): 
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=120)
    obligatorio = models.BooleanField()
    salon = models.ForeignKey(Salon, on_delete = models.CASCADE)

    def agregarServicio (self, nombre, descripcion, obligatorio, salon): 
        self.nombre = nombre 
        self.descripcion = descripcion 
        self.obligatorio = obligatorio 
        self.salon = salon 
        self.save() 

    def __str__(self):
        return f'id={self.id}, nombre={self.nombre}, descripcion={self.descripcion}, obligatorio={self.obligatorio}'

class Alquiler (models.Model): 
    salon = models.ForeignKey(Salon, on_delete = models.CASCADE)
    afiliado = models.ForeignKey(Afiliado, on_delete = models.CASCADE)
    seña = models.FloatField(max_length = 8)
    reserva = models.DateField() 
    inicio = models.DateField( null = True, blank = True) 

    def agregarAlquiler (self, salon, seña, reserva, inicio, afiliado): 
        self.salon = salon 
        self.afiliado = afiliado 
        self.seña = seña 
        self.reserva = reserva 
        if (inicio.len != 0): 
            self.inicio = inicio
        self.save()

class PagoAlquiler (models.Model): 
    TIPOPAGO = [(0, "debito"), (1, "credito"), (2, "efectivo")]
    alquiler = models.ForeignKey(Alquiler, on_delete = models.CASCADE)
    pago = models.DateField() 
    monto = models.FloatField(max_length = 6)
    formaPago = models.PositiveBigIntegerField(choices = TIPOPAGO)
    
    
    def agregarPago (self, alquiler, pago, monto, formaPago):
        self.alquiler = alquiler 
        self.pago = pago 
        self.monto = monto 
        self.formaPago = formaPago 
        self.save() 

