
import this
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    dni = models.CharField(max_length=8)
    nombre = models.CharField(max_length= 30)
    apellido = models.CharField(max_length= 30)
    fechaNacimiento = models.DateField()
    usuario = models.OneToOneField(User, null = True, blank = True,  on_delete = models.CASCADE) 
    es_afiliado = models.BooleanField(default = False) 
    es_alumno = models.BooleanField(default = False) 
    es_profesor=models.BooleanField(default=False)
    es_encargado=models.BooleanField(default=False)

    def afiliar(self, afiliado, fecha):
        assert not self.es_afiliado, "Ya soy afiliado" 
        afiliado.desde = fecha
        afiliado.persona = self
        afiliado.save()
        self.es_afiliado=True
        self.save()

    def desafiliar(self, afiliado, fecha):
        assert afiliado.persona == self, "Afiliado no existe o es incorrecto"
        afiliado.hasta = fecha
        afiliado.save()
        self.es_afiliado = False
        self.save()
        
    def inscribir(self, alumno, curso):
        assert alumno.curso == curso, "Alumno ya inscripto en el curso"
        alumno.persona = self
        alumno.save()
        curso.alumnos.add(alumno)
        self.es_alumno=True
        self.save()

    def desinscribir(self, alumno, fecha):
        assert alumno.persona == self, "Alumno equivocado o inexistente"
        alumno.hasta = fecha
        alumno.save()
        self.es_alumno = False
        self.save()
    

    def inscribirProfesor (self, profesor, curso): 
        assert profesor.persona == self, "Profesor ya existente en el curso" 
        profesor.persona = self 
        profesor.save() 
        curso.profesores.add(profesor)
        self.es_profesor = True
        self.save() 

    def desinscribirProfesor (self, profesor, fecha): 
        assert profesor.persona == self, "Profesor no existe o profesor equivocado" 
        profesor.hasta = self 
        profesor.save() 
        self.es_profesor = False
        self.save() 

    def serEncargado (self, fecha):
        assert not self.es_encargado, "Ya soy encargado" 
        self.desde = fecha
        self = self
        self.save()
        self.es_encargado = True
        self.save()


    def desinscribirEncargado (self, fecha): 
        assert self == self, "Encargado equivocado"
        self.hasta = fecha
        self.save() 
        self.es_encargado = False 
        self.save() 

    def __str__(self):
        return f'id={self.id}, dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}'


class Vinculo (models.Model): 
    TIPO = [(0, "Conyuge"), (1,"Hijo"), (2,"Tutor")] 
    tipoVinculo = models.PositiveSmallIntegerField(choices = TIPO)
    vinculante = models.ForeignKey(Persona, related_name = "vinculantes", on_delete = models.CASCADE) 
    vinculado = models.ForeignKey(Persona, related_name = "vinculados",  on_delete = models.CASCADE) 



class Rol(models.Model):
    TIPO = 0
    TIPOS = []
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    desde = models.DateTimeField(auto_now_add=True)
    hasta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.persona} es {self.get_tipo_display()}"

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
