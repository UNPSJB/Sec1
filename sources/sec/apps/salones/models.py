from unittest.util import _MAX_LENGTH
from django.db import models

from apps.personas.models import Persona
from apps.afiliados.models import Afiliado


class Salon(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    capacidad = models.PositiveIntegerField()
    monto = models.FloatField(max_length=9)
    encargado = models.ForeignKey(Persona, on_delete = models.CASCADE)
    afiliado = models.ManyToManyField(Afiliado, through = 'Alquiler')

    def alquilar(self, afiliado, senia, reserva, inicio,monto):
        alquiler = Alquiler.objects.create(alquiler, self, senia, reserva, inicio, afiliado, monto)
        self.save() 

    def __str__(self):
        return f'{self.nombre}'

class Servicio(models.Model): 
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=120)
    obligatorio = models.BooleanField(default = False)
    salon = models.ForeignKey(Salon, on_delete = models.CASCADE, related_name='servicios')

    def __str__(self):
        return f'{self.nombre}'

class Alquiler (models.Model): 
    salon = models.ForeignKey(Salon, on_delete = models.CASCADE)
    afiliado = models.ForeignKey(Afiliado, on_delete = models.CASCADE)
    senia = models.FloatField()
    reserva = models.DateField() 
    inicio = models.DateField( null = True, blank = True)
    monto = models.FloatField()
    ESTADO_PAGO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
    ]
    estado_pago = models.CharField(max_length=10, choices=ESTADO_PAGO_CHOICES, default='PENDIENTE')

class PagoAlquiler (models.Model): 
    TIPOPAGO = [(0, "debito"), (1, "credito"), (2, "efectivo")]
    alquiler = models.ForeignKey(Alquiler, on_delete = models.CASCADE)
    pago = models.DateField() 
    monto = models.FloatField(max_length = 9)
    formaPago = models.PositiveSmallIntegerField(choices = TIPOPAGO)
    
class PagoUnico(models.Model):
    alquiler = models.ForeignKey(Alquiler, on_delete = models.CASCADE)
    pago = models.DateField()
    monto = models.DecimalField(max_digits=9,decimal_places=2)
    
class PagoCuota(models.Model):
    alquiler = models.ForeignKey(Alquiler, on_delete = models.CASCADE)
    num_cuotas = models.IntegerField()
    monto = models.DecimalField(max_digits=9,decimal_places=2)
    pago = models.DateField()
