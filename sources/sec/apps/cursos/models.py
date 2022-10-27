from statistics import mode
from django.db import models
from apps.personas.models import Rol 
from apps.personas.models import Persona

class Curso(models.Model):
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()
    cupo = models.IntegerField(2)
    modulos = models.IntegerField(2)
    descuento = models.IntegerField(2)
    precio = models.IntegerField(4)

    def __str__(self):
        return f'fechaDesde={self.fechaDesde}, fechaHasta={self.fechaHasta}, cupo={self.cupo}, modulos={self.modulos}, descuento={self.descuento}, precio={self.precio}'


class Aula(models.Model): 
    nroAula = models.PositiveIntegerField(max_length=30)
    capacidad = models.PositiveIntegerField(max_length=2)

def __str__ (self): 
    return f'id={self.id}, nroAula={self.nroAula}, capacidad={self.capacidad}'


class Profesor(Rol):
    TIPO = 2
    dni = models.CharField(max_length=8)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    especializacion = models.CharField(max_length=30)
    añosExperiencia = models.IntegerField(max_length=2)
    cbu: models.IntegerField(max_length=20)
    fechaDesde = models.DateField() 
    fechaHasta = models.DateField()

    def __str__(self):
        return f'id={self.id}, dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}, domicilio={self.domicilio}, telefono={self.telefono}, especializacion={self.especializacion}, añosExperiencia={self.añosExperiencia}, cbu={self.cbu}'

class Alumno (Rol): 
    TIPO = 3
    curso= models.OneToOneField(Curso, on_delete = models.CASCADE, parent_link = True)
    responsable= models.OneToOneField(Persona, on_delete = models.CASCADE, parent_link = True) 

    


class Dictado(models.Model): 
    aula = models.ManyToManyField(Aula)
    cursos = models.ForeignKey(Curso, on_delete = models.CASCADE)
    profesores = models.ManyToManyField(Profesor, through = 'Titular') 
    costo = models.FloatField(max_length=10)
    fechaInicio = models.DateField()
    fechaFin = models.DateField() 

class Titular (models.Model): 
    profesor = models.ForeignKey(Profesor, on_delete = models.CASCADE)
    dictado = models.ForeignKey(Dictado, on_delete = models.CASCADE)

def __str__(self):
    return f'id={self.id}, aula={self.aula}, cursos={self.cursos}, profesores={self.profesores}, costo={self.costo}, fechaInicio={self.fechaInicio}, fechaFin = {self.fechaFin}'


