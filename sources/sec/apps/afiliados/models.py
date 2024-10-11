from django.db import models
from apps.personas.models import Rol, Persona
from datetime import datetime


class Comercio(models.Model):
    cuit = models.CharField(max_length=11, unique = True)
    razonSocial = models.CharField(max_length=50)
    rama = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)

    def __str__(self):
        return f'cuit={self.cuit}, razonSocial={self.razonSocial}'


class Afiliado(Rol):
    TIPO = Persona.ROL_AFILIADO
    cuil = models.CharField(max_length=11) 
    ingresoTrabajo = models.DateField()
    sueldo = models.FloatField(max_length=50)
    jornadaLaboral = models.CharField(max_length=2) 
    comercio = models.ForeignKey(Comercio, on_delete = models.CASCADE)
    alta = models.DateField(null= True, blank= True)
    observacion = models.CharField(max_length=100,null= True, blank= True)

    def estado(self):
        if self.hasta is not None and self.alta is not None:
            return 'Desafiliado'
        elif self.hasta is not None and self.alta is None:
            return 'Rechazado'
        elif self.hasta is None and self.alta is None:
            return 'Pendiente'
        elif self.hasta is None and self.alta is not None:
            return 'Activo'
        return 'Estado desconocido'  # Opcional, por si acaso no cae en ninguna de las condiciones

    def darAlta(self):
        assert not self.persona.es_afiliado, "Ya soy afiliado" 
        fecha= datetime.now()
        self.alta = fecha
        self.persona.es_afiliado=True
        self.persona.save()
        self.save()
    
    def desafiliar(self,motivo):
        assert not self.hasta, "Ya estoy desafiliado"
        fecha= datetime.now()
        self.hasta = fecha
        self.observacion = motivo 
        self.persona.es_afiliado = False
        familiares = self.familiares.all()
        for familiar in familiares:
            familiar.dejarDeSer()
        self.persona.save() 
        self.save()

    def rechazar(self,motivo):
        fecha= datetime.now()
        self.hasta = fecha
        self.observacion = motivo 
        self.save()
    

    def __str__(self):
        return f'{self.persona.nombre} {self.persona.apellido}'

Rol.register(Afiliado)

class Familiar(Rol):
    TIPO = Persona.ROL_FAMILIAR
    RELACION = [(0,"Cónyuge"), (1,"Hijo/a")]
    relacion = models.PositiveSmallIntegerField(choices=RELACION)
    vinculante = models.ForeignKey(Afiliado, related_name="familiares",on_delete = models.CASCADE)

    def dejarDeSer(self):
        fecha= datetime.now()
        self.persona.es_familiar = False
        self.persona.save()
        # self.hasta = fecha #Con esto era softdelete
        # self.save()
        self.delete()

Rol.register(Familiar)
