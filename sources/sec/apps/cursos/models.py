from django.db import models
from apps.personas.models import Rol, Persona
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
        return f'{self.nombre}'

class Aula(models.Model): 
    numero = models.PositiveIntegerField(max_length=2, primary_key = True)
    capacidad = models.PositiveIntegerField(max_length=3)

    #Revisar
    def agregarAula (self, numero, capacidad): 
        self.numero = numero 
        self.capacidad = capacidad 
        self.save() 


    def __str__ (self): 
        return f'{self.numero}'


class Profesor(Rol):
    TIPO = Persona.ROL_PROFESOR
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=13)
    especializacion = models.ForeignKey(Especialidad, on_delete = models.CASCADE)
    aniosExperiencia = models.PositiveIntegerField(max_length=2)
    cbu = models.PositiveIntegerField(max_length=22, unique = True)


    def serProfesor(self):
        assert not self.es_profesor, "ya soy Profesor" 
        self.persona = self
        self.save()
        self.persona.es_profesor = True
        self.save()

    def inscribirProfesor (self, dictado): 
        assert dictado.profesor == self, "Profesor ya existente en el dictado" 
        dictado.profesores.add(self) 
        self.save() 

    #Revisar
    def agregarProfesor (self, domicilio, telefono, especializacion, aniosExperiencia, cbu): 
        self.domicilio = domicilio
        self.telefono = telefono 
        self.especializacion = especializacion
        self.aniosExperiencia = aniosExperiencia
        self.cbu = cbu
        self.serProfesor(self)
        self.save()


    def __str__(self):
        return f'{self.persona.nombre} {self.persona.apellido} {self.persona.dni}'

Rol.register(Profesor)

class Curso(models.Model):
    TIPO = [(0, "Clase"), (1, "Mensual")]
    nombre = models.CharField(max_length = 100, primary_key = True)
    desde = models.DateField()
    hasta = models.DateField()
    cupo = models.PositiveIntegerField(max_length = 20)
    cantModulos = models.PositiveIntegerField( max_length = 20)
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
        return f'{self.nombre}, ${self.precio}'


class Dictado(models.Model): 
    aula = models.ManyToManyField(Aula)
    curso = models.ForeignKey(Curso, on_delete = models.CASCADE)
    profesor = models.ManyToManyField(Profesor, through = 'Titularidad')
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


    def inscribirAlumnoADictado (self, persona): 
        curso = self.curso
        persona = Alumno()
        persona = Alumno.inscribirACurso(persona, curso, self)
        self.save() 


    def __str__(self):
        return f'{self.curso}, {self.profesor}'


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

    def __str__(self): 
        return f'{self.dia}, {self.inicio}, {self.fin}'

class Alumno (Rol): 
    TIPO = Persona.ROL_ALUMNO
    curso = models.ForeignKey(Curso, related_name= 'alumnos', on_delete = models.CASCADE)
    dictado = models.ManyToManyField(Dictado, blank= True , through = "PagoDictado")

    def inscribirACurso(self, curso, dictado):
        assert self.curso == curso, "Alumno ya inscripto en el curso"
        self.curso = curso
        self.dictado = dictado
        self.save()
        curso.self.add(self) 
        self.persona.es_alumno = True
        self.save()

    def desinscribirDeCurso(self, fecha):
        assert self.persona == self, "Alumno equivocado o inexistente"
        self.persona.es_alumno = False 
        self.hasta = fecha
        self.save()


    @property
    def responsable(self):
        # Un Responsables de alumno es su padre, su madre o un tutor
        esTutor = models.Q(tipo=Vinculo.TUTOR)
        esPadre = models.Q(tipo = Vinculo.PADRE) 
        esMadre = models.Q(tipo = Vinculo.MADRE)
        vinculo = self.persona.vinculantes.filter(esPadre | esMadre | esTutor).first()
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

    def __str__(self): 
        return f'{self.pago}, ${self.monto}'

class Titularidad (models.Model): 
    profesor = models.ForeignKey(Profesor, on_delete = models.CASCADE)
    dictado = models.ForeignKey(Dictado, on_delete = models.CASCADE)
    desde = models.DateField() 
    hasta = models.DateField(null = True, blank = True) 

    #Revisar
    def agregarTitularidad (self, profesor, curso, desde, hasta = None): 
        self.profesor = profesor 
        self.curso = curso 
        self.desde = desde 
        self.hasta = hasta
        self.save() 

    def __str__ (self): 
        return f'Profesor= {self.profesor.persona.__str__}, Desde: {self.desde}'

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

    def __str__(self): 
        return f'{self.liquidacion}, ${self.monto}'

class AsistenciaProfesor (models.Model): 
    asistencia = models.DateField()
    titular = models.ForeignKey(Titularidad, on_delete = models.CASCADE)

    #Revisar
    def agregarAsistencia (self, asistencia, titular): 
        self.asistencia = asistencia 
        self.titular = titular
        self.save()

    def __str__(self): 
        return f'{self.asistencia}'
