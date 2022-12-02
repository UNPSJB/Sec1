from django.db import models
from apps.personas.models import Rol, Persona
from apps.personas.models import Vinculo
from datetime import date
MAYEDAD = 18 

class Especialidad (models.Model): 
    AREA = [(0, "Capacitacion"), (1, "Cultura"), (2, "Gimnasio")]
    nombre = models.CharField(unique = True, max_length = 20)
    area = models.PositiveSmallIntegerField(choices = AREA)

    def __str__ (self): 
        return f'{self.nombre}'

class Aula(models.Model): 
    numero = models.PositiveIntegerField(max_length=2, unique = True)
    capacidad = models.PositiveIntegerField(max_length=3)

    def __str__ (self): 
        return f'{self.numero}'

class Profesor(Rol):
    TIPO = Persona.ROL_PROFESOR
    especializacion = models.ForeignKey(Especialidad, on_delete = models.CASCADE)
    aniosExperiencia = models.PositiveIntegerField(max_length=2)
    cbu = models.PositiveIntegerField(max_length=22, unique = True)


    def registrarAsistencia (self, fecha):
        for t in self.dictados.filter(hasta__isnull = True ):
            dictado = t.dictado
            clases = dictado.clases.all() 
            for c in clases: 
                if (c.dia == fecha.isoweekday()): 
                    t.agregarAsistencia(fecha)

    def __str__(self):
        return f'{self.persona.nombre} {self.persona.apellido}'

Rol.register(Profesor)

class Curso(models.Model):
    TIPO = [(0, "Clase"), (1, "Mensual")]
    TIPOMODULO = [(0, "Por clase"), (1, "Por mes"), (2, "Total")]
    nombre = models.CharField(max_length = 100)
    desde = models.DateField()
    hasta = models.DateField()
    cupo = models.PositiveIntegerField(max_length = 20, help_text= 'Cupo minimo de alumnos para iniciar dictado')
    modulos = models.PositiveIntegerField( max_length = 20, help_text = 'Cantidad de horas. 1 modulo = 1 hora')
    tipoModulo = models.PositiveSmallIntegerField(choices = TIPOMODULO)
    descuento = models.PositiveIntegerField(max_length = 2)
    precio = models.PositiveIntegerField(max_length = 4)
    formaPago = models.PositiveSmallIntegerField(choices = TIPO)
    especialidad = models.ForeignKey(Especialidad, on_delete = models.CASCADE)

    def alumnosEnEsperaPriorizados(self):
        #TODO: priorizar alumnos en espera
        return self.alumnos.all()
    
    def __str__(self):
        return f'{self.nombre}, ${self.precio}'

class Dictado(models.Model): 
    aula = models.ForeignKey(Aula, on_delete = models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete = models.CASCADE)
    profesores = models.ManyToManyField(Profesor, through = 'Titularidad')
    costo = models.FloatField(max_length=10)
    cupo = models.PositiveIntegerField(max_length = 20)
    inicio = models.DateField()
    fin = models.DateField() 

    def comenzo(self):
        return self.inicio <= date.today()

    def finalizo(self):
        return self.fin <= date.today()



    def agregarTitularidad(self, profesor, desde):
        return Titularidad.objects.create(profesor=profesor,
                                        desde=desde,
                                        dictado=self)


    def agregarClase (self, horaInicio, horaFin, dia): 
        return Clase.objects.create(inicio = horaInicio, fin=horaFin, dia = dia, dictado = self)


    def cambiarTitularidad (self, profesor, desde):
        titular = self.titulares.filter(hasta__isnull = True).first()
        assert titular != None, "Debe existir al menos un titular" 
        assert titular.profesor != profesor, "El profesor ya es titular"
        titular.hasta = desde
        titular.save() 
        return self.agregarTitularidad(profesor,desde) 

    def __str__(self):
        return f'{self.curso}, {self.profesores.all()}, {self.aula}'


class Clase (models.Model): 
    DIA = [(1,"Lunes"), (2, "Martes"), (3, "Miercoles"), (4, "Jueves"), (5, "Viernes")]
    inicio = models.TimeField() 
    fin = models.TimeField() 
    dia = models.PositiveSmallIntegerField(choices = DIA)
    dictado = models.ForeignKey(Dictado, related_name = "clases", on_delete = models.CASCADE)


    def __str__(self): 
        return f'{self.dia}, {self.inicio}, {self.fin}'

class Alumno (Rol): 
    TIPO = Persona.ROL_ALUMNO
    curso = models.ForeignKey(Curso, related_name= 'alumnos', on_delete = models.CASCADE)
    dictado = models.ForeignKey(Dictado, blank= True, null = True, on_delete = models.CASCADE)

    def agregarResponsable (self, persona, tipoResponsable): 
        if ((date.today() - self.persona.nacimiento ) < MAYEDAD): 
            return Vinculo.objects.create (tipo = tipoResponsable, vinculante = self, vinculado = persona)


    """
    def inscribirADictado (self, dictado, fechaPago, monto, tipoPago): 
        assert self.dictado != dictado, "Alumno ya inscripto en el dictado"
        return PagoDictado.objects.create(dictado = dictado, alumno = self, pago = fechaPago,
        monto = monto, tipoPago = tipoPago) 
    """
    def inscribirADictado (self, dictado): 
        #assert self.dictado != dictado, "Alumno ya inscripto en el dictado"
        self.dictado = dictado
        self.save()

    def desinscribiDeDictado (self): 
        #assert self.dictado != dictado, "Alumno ya inscripto en el dictado"
        self.dictado = None
        self.save()  

    def inscribir(self, persona, curso):
        #assert not self.curso == curso, "Alumno ya inscripto al curso"
        self.persona = persona
        self.curso = curso
        self.save()
        curso.alumnos.add(self) 
        persona.es_alumno = True
        persona.save()
       
    def desinscribir(self, persona, curso, fecha):
        assert self.persona == persona, "Alumno no existe" 
        assert self.curso == curso, "Alumno no pertenece al curso"
        self.hasta = fecha
        self.save()
        persona.es_alumno = False
        persona.save() 

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

    def __str__(self): 
        return f'{self.pago}, ${self.monto}'

class Titularidad (models.Model): 
    profesor = models.ForeignKey(Profesor, related_name= "dictados",  on_delete = models.CASCADE)
    dictado = models.ForeignKey(Dictado, related_name = "titulares", on_delete = models.CASCADE)
    desde = models.DateField() 
    hasta = models.DateField(null = True, blank = True) 

    def agregarAsistencia (self,fecha): 
        return AsistenciaProfesor.objects.create(asistencia = fecha, titular = self)

    def agregarPagoTitular (self, monto, fechaLiquidacion): 
        return Liquidacion.objects.create(liquidacion = fechaLiquidacion, monto = monto, titular = self)


    def __str__ (self): 
        return f'Profesor= {self.profesor}, Desde: {self.desde}'

class Liquidacion (models.Model): 
    liquidacion = models.DateField()
    monto = models.FloatField(max_length = 4) 
    titular = models.ForeignKey(Titularidad, on_delete = models.CASCADE)

    def __str__(self): 
        return f'{self.liquidacion}, ${self.monto}'

class AsistenciaProfesor (models.Model): 
    asistencia = models.DateField()
    titular = models.ForeignKey(Titularidad, related_name = "asistencia", on_delete = models.CASCADE)

    def __str__(self): 
        return f'{self.asistencia}'
