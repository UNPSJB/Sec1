from unittest.util import _MAX_LENGTH
from django.db import models
import os
from django.conf import settings

from apps.personas.models import Persona
from apps.afiliados.models import Afiliado

from django.utils import timezone

class Salon(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    capacidad = models.PositiveIntegerField()
    monto = models.FloatField(max_length=9)
    encargado = models.ForeignKey(Persona, on_delete = models.CASCADE)
    imagen = models.ImageField(upload_to='static/img', null=True)
    imagen2 = models.ImageField(upload_to='static/img', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='static/img', blank=True, null=True)
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
    cancelado = models.BooleanField(default=False)
    pago_senia = models.DateField(blank=True,null=True)
    
    @property
    def tiene_cuotas(self):
        return self.pagoalquiler_set.exists()
    
    def estado_cuotas(self):
        
        if not self.pagoalquiler_set.exists():
            return False
        
        return all(pago.pago is not None for pago in self.pagoalquiler_set.all())

    def estado_alquiler(self):
        if self.estado_cuotas():
            if self.inicio < timezone.now().date():
                return "Concluido"  # Todas las cuotas pagadas y la fecha de inicio ha pasado
            else:
                return "Pagado"  # Todas las cuotas pagadas, pero no ha pasado la fecha de inicio
        else:
            if self.inicio < timezone.now().date():
                self.cancelado = True
                return "Cancelado"  # No pago las cuotas y paso la fecha
            else:
                return "Pendiente"  # No todas las cuotas están pagadas o no hay cuotas creadas
class PagoAlquiler(models.Model):
    alquiler = models.ForeignKey(Alquiler, on_delete = models.CASCADE)
    cuotas = models.IntegerField(default=1) #numero de cuotas totales/ seleccionables
    monto = models.DecimalField(max_digits=9,decimal_places=2)
    pago = models.DateField( null = True, blank = True)
    numero = models.IntegerField(default=1) #numero de cuota

    def puede_pagar(self):
        # Si es la primera cuota, siempre puede pagarse
        if self.numero == 1:
            return True

        # Verificar si la cuota anterior ha sido pagada
        cuota_anterior = PagoAlquiler.objects.filter(alquiler=self.alquiler, numero=self.numero - 1).first()
        return cuota_anterior is not None and cuota_anterior.pago is not None
