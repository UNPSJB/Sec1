from django.db import models
from apps.personas.models import Rol


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

def __str__(self):
    return f'tipo={self.TIPO}, cuil={self.cuil}, nacionalidad={self.nacionalidad}, estadoCivil={self.estadoCivil}, domicilio={self.domicilio}, telefono={self.telefono}, email={self.email}, fechaIngresoTrabajo={self.fechaIngresoTrabajo}, sueldo={self.sueldo}, JornadaLaboral={self.JornadaLaboral}'

class Empresa(models.Model):
    cuit = models.CharField(max_length=50)
    razonSocial = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    domicilioEmpresa = models.CharField(max_length=50)

def __str__(self):
    return f'cuit={self.cuit}, razonSocial={self.razonSocial}, rama={self.rama}, domicilioEmpresa={self.domicilioEmpresa}'
