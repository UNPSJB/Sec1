from django.db import models,transaction
from django.conf import settings
from apps.personas.models import Rol, Persona
from datetime import date
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone
MAYEDAD = 18 

class Aula(models.Model): 
    numero = models.CharField(max_length=2, unique = True)
    capacidad = models.CharField(max_length=3)
    baja = models.DateField(null=True, blank=True)

    def __str__ (self): 
        return f'{self.numero}'

class Profesor(Rol):
    TIPO = Persona.ROL_PROFESOR
    experiencia = models.CharField(max_length = 300)
    cbu = models.CharField(max_length=22, unique = True)
    #cv

    def actividadesVigentes(self):
        return self.dictados.filter(fin__gt=datetime.now().date())

    def __str__(self):
        return f'{self.persona.nombre} {self.persona.apellido}'

Rol.register(Profesor)

class Actividad(models.Model):
    nombre = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 300)
    desde = models.DateField(default= datetime.now)
    hasta = models.DateField(null=True, blank=True)
    descuento = models.CharField(max_length = 2,help_text = 'Expresado en porcentaje')
    TIPO = [(0, "Capacitacion"), (1, "Cultura"), (2, "Gimnasio Saludable")]
    categoria = models.PositiveSmallIntegerField(choices = TIPO)
    TIPOABONO = [(0, "Por clase"), (1, "Por mes")]
    tipoAbono = models.PositiveSmallIntegerField(choices = TIPOABONO)
    cupoReferencia = models.CharField(max_length = 2)
    precioReferencia = models.FloatField(max_length = 4)
    remuneracionProfesor = models.FloatField(max_length = 4)
    diasTolerancia = models.CharField(max_length = 2,default=0 ,null=True,help_text = 'Solo aplica a actividades de Capacitacion')
    #foto
    
    def baja(self):
        self.hasta = datetime.now().date()
        self.save()


    def __str__(self):
        return f'{self.nombre}'


DIA = [
    (0, "Lunes"),
    (1, "Martes"),
    (2, "Miércoles"),
    (3, "Jueves"),
    (4, "Viernes"),
    (5, "Sábado"),
]
DIA_DICT = {name: number for number, name in DIA}
class Dictado(models.Model): 
    aula = models.ForeignKey(Aula, on_delete = models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete = models.CASCADE)
    profesor = models.ForeignKey(Profesor, related_name = "dictados", on_delete = models.CASCADE)
    costo = models.FloatField(max_length=10)
    cupo = models.CharField(max_length = 20)
    inicio = models.DateField()
    fin = models.DateField()
    duracionClase = models.CharField(max_length=1,help_text = 'Cantidad de horas')
    horaInicioClase = models.TimeField() 
    # Campo para almacenar días como una cadena
    dias = models.CharField(max_length=50, blank=True)

    def cupoDisponible(self):
        return int(self.cupo) - self.inscripciones.filter(estado=0).count()

    def estado(self):
        if self.fin <= datetime.now().date():
            return "Finalizado"
        else:
            if self.actividad.tipoAbono == 0:
                return "Abierto"
            else: 
                if self.actividad.categoria == 0:
                    finInscripciones = self.actividad.desde + timedelta(days=int(self.actividad.diasTolerancia))
                    if finInscripciones < datetime.now().date():
                        return "Cerrado"
                    else:
                        if self.cupoDisponible() == 0:
                            return "Sin Cupo"
                        else:
                            return "Abierto"
                else:
                    if self.cupoDisponible() == 0:
                            return "Sin Cupo"
                    else:
                            return "Abierto"

    def generar_clases(self):
        # Convierte la cadena de días en una lista de enteros
        dias_seleccionados = list(map(str, self.dias.split(','))) if self.dias else []
        numeros_dias = [DIA_DICT[dia] for dia in dias_seleccionados if dia in DIA_DICT]
        fecha_inicio = self.inicio
        hora_inicio=self.horaInicioClase
        inicio_clase = datetime.combine(fecha_inicio, hora_inicio)
        duracionClase = int(self.duracionClase)
        #fin_clase = inicio_clase + timedelta(hours=duracionClase)
        clases_a_crear = []  # Lista para almacenar las instancias de Clase

        while inicio_clase.date() <= self.fin:
            # Comprueba si el día actual es uno de los días seleccionados
            if inicio_clase.weekday() in numeros_dias:
                # Agrega una nueva instancia de Clase a la lista
                clases_a_crear.append(Clase(dictado=self, inicio=inicio_clase, fin=(inicio_clase+timedelta(hours=duracionClase))))
            inicio_clase += timedelta(days=1)

        # Realiza la creación en bloque
        if clases_a_crear:
            with transaction.atomic():  # Asegura que todo se ejecute como una sola transacción
                Clase.objects.bulk_create(clases_a_crear)

    def generar_sueldo_profesor(self):
        hoy = datetime.now().date()
        # Crear una lista para almacenar las instancias de Pago
        pagos = []
        monto= self.actividad.remuneracionProfesor

        # Calcular el primer día del mes siguiente
        primer_dia_mes_siguiente = (self.inicio.replace(day=1) + timedelta(days=32)).replace(day=1)

        # Verificar que la fecha_final no sea anterior al primer día del mes siguiente
        if self.fin > primer_dia_mes_siguiente:
            # Crear pagos desde el primer día del mes siguiente hasta la fecha final
            fecha_actual = primer_dia_mes_siguiente

            while fecha_actual <= self.fin:
                # Crear una nueva instancia de Pago
                pago = Liquidacion(liquidacion=fecha_actual,dictado=self, monto=monto)
                pagos.append(pago)  # Añadir la instancia a la lista
                # Incrementar la fecha por un mes
                fecha_actual += relativedelta(months=1)

        # Usar bulk_create para insertar todas las instancias a la vez
        Liquidacion.objects.bulk_create(pagos)

    def finalizo(self):
        return self.fin <= date.today()


    def inscripciones_activas(self):
        return self.inscripciones.filter(estado=0)

    def inscripciones_en_espera(self):
        return self.inscripciones.filter(estado=1)


    def __str__(self):
        return f'{self.actividad.nombre}'


class Clase (models.Model): 
    inicio = models.DateTimeField() 
    fin = models.DateTimeField() 
    dictado = models.ForeignKey(Dictado, related_name = "clases", on_delete = models.CASCADE)
    ESTADOS = [(0, "Pendiente"), (1, "Dictada")]
    estado = models.PositiveSmallIntegerField(choices = ESTADOS, default=0)

    def noEsDelFuturo(self):
        return self.inicio <= timezone.now()

    def __str__(self): 
        return f'{self.inicio}, {self.fin}'


class Alumno (Rol): 
    TIPO = Persona.ROL_ALUMNO

    def esta_inscrito_en_dictado(self, dictadoId):
        return self.inscripciones.filter(Q(dictado=dictadoId) & Q(estado__in=[0, 1])).exists()

    def esta_inscrito_en_clase(self, claseId):
        return self.inscripciones.filter(clase=claseId).exists()

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

Rol.register(Alumno)

class Inscripcion(models.Model):
    dictado = models.ForeignKey(Dictado, related_name = "inscripciones", on_delete = models.CASCADE,null=True)
    clase = models.ForeignKey(Clase, on_delete = models.CASCADE,null=True)
    alumno = models.ForeignKey(Alumno, related_name = "inscripciones", on_delete = models.CASCADE)
    ESTADO = [(0, "Inscripto"), (1, "En Espera"), (2, "Cancelado")]
    estado = models.PositiveSmallIntegerField(choices = ESTADO, default=1)

    def inscribir(self):
        self.estado = 0
        self.save()
        hoy = datetime.now().date()
        # Crear una lista para almacenar las instancias de Pago
        pagos = []
        monto= self.dictado.costo
        if self.alumno.persona.es_afiliado:
            monto = monto-(monto*(int(self.dictado.actividad.descuento)/100))
        pago = Pago(inscripcion=self,fecha=hoy,pago=hoy,monto=monto)
        pagos.append(pago)
        # Calcular el primer día del mes siguiente
        primer_dia_mes_siguiente = (hoy.replace(day=1) + timedelta(days=32)).replace(day=1)

        # Verificar que la fecha_final no sea anterior al primer día del mes siguiente
        if self.dictado.fin > primer_dia_mes_siguiente:
            # Crear pagos desde el primer día del mes siguiente hasta la fecha final
            fecha_actual = primer_dia_mes_siguiente

            while fecha_actual <= self.dictado.fin:
                # Crear una nueva instancia de Pago
                pago = Pago(inscripcion=self,fecha=fecha_actual, monto=monto)
                pagos.append(pago)  # Añadir la instancia a la lista
                # Incrementar la fecha por un mes
                fecha_actual += relativedelta(months=1)

        # Usar bulk_create para insertar todas las instancias a la vez
        Pago.objects.bulk_create(pagos)

    def inscribir_clase(self):
        self.estado = 0
        self.save()
        hoy = datetime.now().date()
        monto= self.clase.dictado.costo
        if self.alumno.persona.es_afiliado:
            monto = monto-(monto*(int(self.clase.dictado.actividad.descuento)/100))
        pago = Pago.objects.create(inscripcion=self,fecha=hoy,pago=hoy,monto=monto)

    def desinscribir(self):
        self.estado= 2
        self.save()




class Pago (models.Model): 
    inscripcion = models.ForeignKey(Inscripcion, related_name = "pagos",on_delete = models.CASCADE)
    fecha = models.DateField() 
    pago = models.DateField(null=True)
    monto = models.FloatField(max_length = 10)

    def pagar(self):
        self.pago = datetime.now().date()
        self.save()


class Liquidacion (models.Model): 
    liquidacion = models.DateField()
    monto = models.FloatField() 
    dictado = models.ForeignKey(Dictado, related_name = "liquidaciones", on_delete = models.CASCADE)
    fechaPago = models.DateField(null=True)

    def pagar(self):
        self.fechaPago = datetime.now().date()
        self.save()

    def __str__(self): 
        return f'{self.liquidacion}, ${self.monto}'

class AsistenciaProfesor (models.Model): 
    asistencia = models.DateField()
    #titular = models.ForeignKey(Titularidad, related_name = "asistencia", on_delete = models.CASCADE)

    def __str__(self): 
        return f'{self.asistencia}'
