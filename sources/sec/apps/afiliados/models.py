from django.db import models
from apps.personas.models import Rol, Persona


class Empresa(models.Model):
    cuit = models.CharField(max_length=13)
    razonSocial = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)

    def __str__(self):
        return f'cuit={self.cuit}, razonSocial={self.razonSocial}, rama={self.rama}, domicilioEmpresa={self.domicilio}'



class Afiliado(Rol):
    TIPO = Persona.ROL_AFILIADO
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

    
    def afiliar( self, fecha=None):
        assert not self.persona.es_afiliado, "Ya soy afiliado" 
        #if  fecha is None:
        #    fecha= datetime.now()
        #afiliado.desde = fecha
        self.persona = self
        self.persona.es_afiliado=True
        self.save()

    def desafiliar(self, fecha):
        assert self.persona == self, "Afiliado no existe o es incorrecto"
        self.hasta = fecha
        self.persona.es_afiliado = False
        self.save()

    def __str__(self):
        return f'{self.persona.nombre} {self.persona.apellido}'

Rol.register(Afiliado)

