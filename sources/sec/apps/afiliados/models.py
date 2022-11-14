from django.db import models
from apps.personas.models import Rol


class Empresa(models.Model):
    cuit = models.CharField(max_length=13)
    razonSocial = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)

    def __str__(self):
        return f'cuit={self.cuit}, razonSocial={self.razonSocial}, rama={self.rama}, domicilioEmpresa={self.domicilioEmpresa}'



class Afiliado(Rol):
    TIPO = 1
    cuil = models.CharField(max_length=13)
    nacionalidad = models.CharField(max_length=50)
    estadoCivil = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length = 254) 
    ingresoTrabajo = models.DateField()
    sueldo = models.FloatField(max_length=50)
    jornadaLaboral = models.CharField(max_length=50) 
    empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE)

    def como (self): 
        if (Rol.TIPO == 1): 
            return ("Es afiliado")

    def __str__(self):
        return f'cuil={self.cuil}'

Rol.register(Afiliado)

