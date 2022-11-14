from django.db import models
from apps.personas.models import Rol 
from apps.personas.models import Vinculo



class Especialidad (models.Model): 
    AREA = [(0, "Capacitacion"), (1, "Cultura"), (2, "Gimnasio")]
    
    nombre = models.CharField(max_length = 20)
    area = models.PositiveSmallIntegerField(choices = AREA)

    #Revisar
    def agregarEspecialidad (self, nombre, area): 
        self.nombre = nombre 
        self.area = area
        self.save() 


    def __str__ (self): 
        return f'nombre={self.nombre}, area = {self.area}'

class Aula(models.Model): 
    numero = models.PositiveIntegerField(max_length=2)
    capacidad = models.PositiveIntegerField(max_length=3)

    #Revisar
    def agregarAula (self, numero, capacidad): 
        self.numero = numero 
        self.capacidad = capacidad 
        self.save() 


    def __str__ (self): 
        return f'numero={self.numero}, capacidad={self.capacidad}'


class Profesor(Rol):
    TIPO = 2
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=13)
    especializacion = models.ForeignKey(Especialidad, on_delete = models.CASCADE)
    aniosExperiencia = models.PositiveIntegerField(max_length=2)
    cbu = models.PositiveIntegerField(max_length=22)


    #Revisar
    def agregarProfesor (self, domicilio, telefono, especializacion, aniosExperiencia, cbu): 
        self.domicilio = domicilio
        self.telefono = telefono 
        self.especializacion = especializacion
        self.aniosExperiencia = aniosExperiencia
        self.cbu = cbu
        self.save()

    def como (self): 
        if (Rol.TIPO == 2): 
            return ("Es profesor")

    def __str__(self):
        return f'nombre={self.persona.nombre}, apellido={self.persona.apellido}'

Rol.register(Profesor)

class Curso(models.Model):
    TIPO = [(0, "Clase"), (1, "Mensual")]
    nombre = models.CharField(max_length = 100)
    desde = models.DateField()
    hasta = models.DateField()
    cupo = models.PositiveIntegerField(max_length = 20)
    cantModulos = models.PositiveIntegerField( max_length = 20)
    profesor = models.ManyToManyField(Profesor, through = 'Titularidad') 
    descuento = models.PositiveIntegerField(max_length = 2)
    precio = models.PositiveIntegerField(max_length = 4)
    formaPago = models.PositiveSmallIntegerField(choices = TIPO)
    especialidad = models.ForeignKey(Especialidad, on_delete = models.CASCADE)

    #Revisar
    def agregarCurso (self, nombre, desde, hasta, cupo, cantModulos, descuento, precio, formaPago, especialidad): 
        self.nombre = nombre 
        self.desde = desde 
        self.hasta = hasta 
        self.cupo = cupo 
        self.cantModulos = cantModulos 
        self.descuento = descuento 
        self.precio = precio 
        self.formaPago = formaPago
        self.especialidad = especialidad
        self.save() 

    def __str__(self):
        return f' nombre = {self.nombre}, fechaDesde={self.desde}, fechaHasta={self.hasta}, descuento={self.descuento}, precio={self.precio}'





class Dictado(models.Model): 
    aula = models.ManyToManyField(Aula)
    curso = models.ForeignKey(Curso, on_delete = models.CASCADE)
    costo = models.FloatField(max_length=10)
    inicio = models.DateField()
    fin = models.DateField() 

    #Revisar
    def agregarDictado (self, curso, costo, inicio, fin): 
        self.curso = curso 
        self.costo = costo 
        self.inicio = inicio 
        self.fin = fin 
        self.save() 


    def __str__(self):
        return f'id={self.id}, aula={self.aula}, cursos={self.cursos}, profesores={self.profesores}, costo={self.costo}, fechaInicio={self.fechaInicio}, fechaFin = {self.fechaFin}'


class Clase (models.Model): 
    DIA = [(1,"Lunes"), (2, "Martes"), (3, "Miercoles"), (4, "Jueves"), (5, "Viernes")]
    inicio = models.TimeField() 
    fin = models.TimeField() 
    dia = models.PositiveSmallIntegerField(choices = DIA)
    dictado = models.ForeignKey(Dictado, on_delete = models.CASCADE)

    #Revisar
    def agregarClase (self, inicio, fin, dia, dictado): 
        self.inicio = inicio 
        self.fin = fin 
        self.dia = dia 
        self.dictado = dictado
        self.save() 


class Alumno (Rol): 
    TIPO = 3
    curso = models.ForeignKey(Curso, on_delete = models.CASCADE)
    dictado = models.ManyToManyField(Dictado, through = "PagoDictado")

    #Revisar
    def agregarAlumno (self, curso, dictado): 
        self.curso = curso 
        self.dictado = dictado
        self.save() 

    def como (self): 
        if (Rol.TIPO == 3): 
            return ("Es alumno") 


    @property
    def responsable(self):
        # Un Responsables de alumno es su padre, su madre o un tutor
        esTutor = models.Q(tipoVinculo=Vinculo.TUTOR)
        esHijo = models.Q(tipoVinculo=Vinculo.HIJO)
        vinculo = self.persona.vinculantes.filter(esTutor | esHijo).first()
        return vinculo.vinculante if vinculo is not None else None

Rol.register(Alumno)

class PagoDictado (models.Model): 
    TIPO = [(0, "Debito"), (1, "Credito"), (2, "Efectivo")]
    dictado = models.ForeignKey(Dictado, on_delete = models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete = models.CASCADE)
    pago = models.DateField() 
    monto = models.FloatField(max_length = 10)
    tipoPago = models.PositiveSmallIntegerField(choices = TIPO)

    #Revisar
    def agregarPago (self, dictado, alumno, pago, monto, tipo):
        self.dictado = dictado 
        self.alumno = alumno 
        self.pago = pago
        self.monto = monto 
        self.tipoPago = tipo
        self.save() 


class Titularidad (models.Model): 
    profesor = models.ForeignKey(Profesor, on_delete = models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete = models.CASCADE)
    desde = models.DateField() 
    hasta = models.DateField(null = True, blank = True) 

    #Revisar
    def agregarTitularidad (self, profesor, curso, desde, hasta): 
        self.profesor = profesor 
        self.curso = curso 
        self.desde = desde 
        self.hasta = hasta
        self.save() 


class Liquidacion (models.Model): 
    liquidacion = models.DateField()
    monto = models.FloatField(max_length = 4) 
    titular = models.ForeignKey(Titularidad, on_delete = models.CASCADE)

    #Revisar 
    def agregarLiquidacion (self, liquidacion, monto, titular): 
        self.liquidacion = liquidacion 
        self.monto = monto 
        self.titular = titular
        self.save() 

class AsistenciaProfesor (models.Model): 
    asistencia = models.DateField()
    titular = models.ForeignKey(Titularidad, on_delete = models.CASCADE)

    #Revisar
    def agregarAsistencia (self, asistencia, titular): 
        self.asistencia = asistencia 
        self.titular = titular
        self.save()

