from django.db import models
from apps.personas.models import Rol


class Empresa(models.Model):
    cuit = models.CharField(max_length=13)
    razonSocial = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    domicilioEmpresa = models.CharField(max_length=50)

    def __str__(self):
        return f'cuit={self.cuit}, razonSocial={self.razonSocial}, rama={self.rama}, domicilioEmpresa={self.domicilioEmpresa}'



class Afiliado(Rol):
    TIPO = 1
    cuil = models.CharField(max_length=13)
    nacionalidad = models.CharField(max_length=50)
    estadoCivil = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)
    teléfono = models.CharField(max_length=50)
    email = models.EmailField(max_length = 254) 
    fechaIngresoTrabajo = models.DateField()
    sueldo = models.FloatField(max_length=50)
    jornadaLaboral = models.CharField(max_length=50) 
    empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE)

    

    def __str__(self):
        return f'tipo={self.TIPO}, cuil={self.cuil}, nacionalidad={self.nacionalidad}, estadoCivil={self.estadoCivil}, domicilio={self.domicilio}, telefono={self.telefono}, email={self.email}, fechaIngresoTrabajo={self.fechaIngresoTrabajo}, sueldo={self.sueldo}, JornadaLaboral={self.JornadaLaboral}'

Rol.register(Afiliado)

