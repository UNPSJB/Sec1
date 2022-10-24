from django.db import models
from apps.personas.models import Rol

# Create your models here.
class Afiliado(Rol):
    TIPO = 1
    cuil = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)
    estadoCivil = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)
    teléfono = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    fechaIngresoTrabajo = models.DateField()
    sueldo = models.CharField(max_length=50)
    JornadaLaboral = models.CharField(max_length=50)

class Empresa(models.Model):
    cuit = models.CharField(max_length=50)
    razonSocial = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    domicilioEmpresa = models.CharField(max_length=50)