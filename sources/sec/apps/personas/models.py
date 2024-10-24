from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
from .nacionalidades import NACIONALIDADES_CHOICES
class PersonaRolManager(models.Manager):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo

    def get_queryset(self):
        return super().get_queryset().filter(roles__tipo=self.tipo)

class PersonaRolQuerySet(models.QuerySet):
    def en_fecha(self, fecha):
        return self.filter(models.Q(roles__desde__lte=fecha) & (models.Q(roles__hasta__gte=fecha) | models.Q(roles__hasta__isnull=True)))

class EncargadoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(es_encargado=True)

#class PersonaRolQuerySet
class Persona(models.Model):
    ROL_AFILIADO = 1
    ROL_ALUMNO= 2
    ROL_PROFESOR= 3
    ROL_ENCARGADO= 4
    ROL_FAMILIAR= 5
    dni = models.CharField(max_length=8, unique = True)
    nombre = models.CharField(max_length= 30)
    apellido = models.CharField(max_length= 30)
    nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=2, choices=NACIONALIDADES_CHOICES)
    ESTADO_CIVIL = [(0, "Casado/a"),(1, "Viudo/a"),(2, "Soltero/a"),(3, "Divorciado/a")] #Esto habria que hacerlo en otro lado
    estadoCivil = models.PositiveSmallIntegerField(choices=ESTADO_CIVIL,null=True)
    domicilio = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length = 254)
    telefono = models.CharField(max_length=15, null=True)
    
    usuario = models.OneToOneField(User, null = True, blank = True,  on_delete = models.CASCADE) 
    es_afiliado = models.BooleanField(default = False) 
    es_alumno = models.BooleanField(default = False) 
    es_profesor=models.BooleanField(default=False)
    es_encargado=models.BooleanField(default=False)
    es_familiar=models.BooleanField(default=False)

    objects = models.Manager()
    afiliados = PersonaRolManager.from_queryset(PersonaRolQuerySet)(1)
    profesores = PersonaRolManager.from_queryset(PersonaRolQuerySet)(3)
    alumnos = PersonaRolManager.from_queryset(PersonaRolQuerySet)(2)
    encargados = EncargadoManager()

    def serProfesor(self):
        assert not self.es_profesor, "Ya soy Profesor" 
        self.es_profesor = True
        self.save()

    def serEncargado (self):
        assert not self.es_encargado, "Ya soy encargado" 
        self.es_encargado = True
        self.save()


    def desinscribirEncargado (self, fecha): 
        assert self == self, "Encargado equivocado o no existe"
        self.hasta = fecha
        self.es_encargado = False 
        self.save() 

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def como(self, ROL, fecha=None, curso = None):
        if fecha == None:
            fecha = datetime.now()
        if curso != None and fecha != None:
            params = models.Q(tipo=ROL) & (models.Q(hasta__isnull=True) | models.Q(hasta__gte=fecha))
            roles = self.roles.filter(params)
        else: 
            roles = self.roles.filter()
        if ROL == self.ROL_ENCARGADO and self.es_encargado:
            return self
        if roles.exists() and ((ROL == self.ROL_AFILIADO or ROL == self.ROL_PROFESOR) or (ROL == self.ROL_ALUMNO and len(roles) == 1)):
            return roles.first().related()
        if roles.exists():
            alumnos = list(filter(lambda a: a.curso == curso, [rol.related() for rol in roles]))
            return alumnos[0] if len(alumnos) == 1 else None

    def es(self, ROL):
        return self.como(ROL) is not None


class Rol(models.Model):
    TIPO = 0
    TIPOS = []
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    desde = models.DateField(default= datetime.now)
    hasta = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.persona}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(Rol, self).save(*args, **kwargs)

    def agregar_rol(self, rol):
        if not self.sos(rol.__class__):
            rol.persona = self
            rol.save()
    
    def sos(self, Klass):
        return any([isinstance(rol, Klass) for rol in self.roles_related()])

    def roles_related(self):
        return [rol.related() for rol in self.roles.all()]

    def related(self):
        return self.__class__ != Rol and self or getattr(self, self.get_tipo_display())

    @classmethod
    def register(cls, klass):
        cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))
