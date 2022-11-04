from django.db import models
from apps.personas.models import Rol 
from apps.personas.models import Vinculo



class Especialidad (models.Model): 
    TIPOAREA = [(0, "Capacitacion"), (1, "Cultura"), (2, "Gimnasio")]
    
    nombre = models.CharField(max_length = 20)
    area = models.PositiveSmallIntegerField(choices = TIPOAREA)

    def __str__ (self): 
        return f'id={self.id}, nombre={self.nombre}'

class Aula(models.Model): 
    nroAula = models.PositiveIntegerField(max_length=30)
    capacidad = models.PositiveIntegerField(max_length=2)

    def __str__ (self): 
        return f'id={self.id}, nroAula={self.nroAula}, capacidad={self.capacidad}'

class Profesor(Rol):
    TIPO = 2
    dni = models.CharField(max_length=11)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    especializacion = models.ForeignKey(Especialidad, on_delete = models.CASCADE)
    añosExperiencia = models.IntegerField(max_length=2)
    cbu: models.IntegerField(max_length=20)

    def __str__(self):
        return f'id={self.id}, dni={self.dni}, nombre={self.nombre}, apellido={self.apellido}, domicilio={self.domicilio}, telefono={self.telefono}, especializacion={self.especializacion}, añosExperiencia={self.añosExperiencia}, cbu={self.cbu}'


class Curso(models.Model):
    TIPO = [(0, "Clase"), (1, "Mensual")]
    nombre = models.CharField(max_length = 10)
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()
    cupo = models.IntegerField(max_length = 20)
    modulos = models.IntegerField( max_length = 20)
    profesores = models.ManyToManyField(Profesor, through = 'Titularidad') 
    descuento = models.IntegerField(max_length = 2)
    precio = models.IntegerField(max_length = 4)
    formaPago = models.PositiveSmallIntegerField(choices = TIPO)
    especialidad = models.ForeignKey(Especialidad, on_delete = models.CASCADE)

    def __str__(self):
        return f'fechaDesde={self.fechaDesde}, fechaHasta={self.fechaHasta}, cupo={self.cupo}, modulos={self.modulos}, descuento={self.descuento}, precio={self.precio}'





class Dictado(models.Model): 
    aula = models.ManyToManyField(Aula)
    curso = models.ForeignKey(Curso, on_delete = models.CASCADE)
    costo = models.FloatField(max_length=10)
    fechaInicio = models.DateField()
    fechaFin = models.DateField() 

    def __str__(self):
        return f'id={self.id}, aula={self.aula}, cursos={self.cursos}, profesores={self.profesores}, costo={self.costo}, fechaInicio={self.fechaInicio}, fechaFin = {self.fechaFin}'


class Clase (models.Model): 
    DIA = [(1,"Lunes"), (2, "Martes"), (3, "Miercoles"), (4, "Jueves"), (5, "Viernes")]
    horaInicio = models.TimeField() 
    horaFin = models.TimeField() 
    dia = models.PositiveSmallIntegerField(choices = DIA)
    dictado = models.ForeignKey(Dictado, on_delete = models.CASCADE)



class Alumno (Rol): 
    TIPO = 3
    curso= models.ForeignKey(Curso, on_delete = models.CASCADE)
    dictado = models.ManyToManyField(Dictado, through = "PagoDictado")


    @property
    def responsable(self):
        vinculo = self.persona.vinculantes.filter(tipo=Vinculo.TUTOR).first()
        return vinculo.vinculante if vinculo is not None else None


class PagoDictado (models.Model): 
    TIPOPAGO = [(0, "Debito"), (1, "Credito"), (2, "Efectivo")]
    dictado = models.ForeignKey(Dictado, on_delete = models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE)
    fechaPago = models.DateField() 
    monto = models.FloatField(max_length = 10)
    tipoPago = models.PositiveSmallIntegerField(choices = TIPOPAGO)


class Titularidad (models.Model): 
    profesor = models.ForeignKey(Profesor, on_delete = models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete = models.CASCADE)
    fechaDesde = models.DateField() 
    fechaHasta = models.DateField(null = True, blank = True) 
    

class Liquidacion (models.Model): 
    fechaLiquidacion = models.DateField()
    monto = models.FloatField(max_length = 4) 
    profesorTitular = models.ForeignKey(Titularidad, on_delete = models.CASCADE)


class AsistenciaProfesor (models.Model): 
    fechaAsistencia = models.DateField()
    profesorTitular = models.ForeignKey(Titularidad, on_delete = models.CASCADE)



