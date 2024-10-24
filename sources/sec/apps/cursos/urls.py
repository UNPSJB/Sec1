from django.urls import path
from .views import *
from apps.cursos import views 
from django.contrib import admin

urlpatterns = [
    #--------------------------------ACTIVIDAD---------------------------------------------
    path('crearActividad/', ActividadCreateView.as_view(), name='crearActividad'),
    path('modificarActividad/<int:pk>', ActividadUpdateView.as_view(), name='modificarActividad'),
    path('detallarActividad/<int:pk>', ActividadDetailView.as_view(), name='detallarActividad'),
    path('listarActividades/', ActividadListView.as_view(), name='listarActividades'),
    path('bajaActividad/', baja_actividad, name='bajaActividad'),
    
    #--------------------------------DICTADO---------------------------------------------
    path('crearDictado/', DictadoCreateView.as_view(), name='crearDictado'),
    path('modificarDictado/<int:pk>', DictadoUpdateView.as_view(), name='modificarDictado'),
    path('eliminarDictado/<int:pk>', DictadoDeleteView.as_view(), name='eliminarDictado'),
    path('detallarDictado/<int:pk>', DictadoDetailView.as_view(), name='detallarDictado'),
    path('listarDictados/', DictadoListView.as_view(), name='listarDictados'),

    #--------------------------------AULA---------------------------------------------
    path('crearAula/', AulaCreateView.as_view(), name='crearAula'),
    path('modificarAula/<int:pk>', AulaUpdateView.as_view(), name='modificarAula'),
    path('eliminarAula/<int:pk>', AulaDeleteView.as_view(), name='eliminarAula'),
    path('listarAulas/', AulaListView.as_view(), name='listarAulas'), 

    #--------------------------------PROFESOR---------------------------------------------
    path('crearProfesor/', crear_profesor, name='crearProfesor'),
    path('buscarPersonaProfesor/',buscar_persona_para_profesor,name='buscarPersonaParaProfesor'),

    #--------------------------------INSCRIPCION---------------------------------------------
    path('inscripcion/<int:dictado_id>', inscripcion_a_dictado, name='inscripcionDictado'),
    path('CrearInscripcionADictado/', crear_inscripcion_a_dictado, name='crearInscripcionDictado'),
    path('inscripcionColaEspera/<int:dictado_id>', inscripcion_a_cola_espera, name='inscripcionColaEspera'),
    path('CrearInscripcionAColaEspera/', crear_inscripcion_a_cola_espera, name='crearInscripcionColaEspera'),
    path('inscripcionClase/<int:clase_id>', inscripcion_a_clase, name='inscripcionClase'),
    path('CrearInscripcionAClase/', crear_inscripcion_a_clase, name='crearInscripcionClase'),
    path('buscarAlumno/',buscar_alumno,name='buscarAlumno'),
    path('detallarInscripcion/<int:pk>', InscripcionDetailView.as_view(), name='detallarInscripcion'),
    path('desinscribir/',desinscribir,name='desinscribir'),
    path('inscribirDesdeEspera/',inscripcion_desde_espera,name='inscribirDesdeEspera'),
    
    #--------------------------------PAGOS---------------------------------------------
    path('listarPagos/', PagoListView.as_view(), name='listarPagos'),
    path('listarPagosProfesor/', LiquidacionListView.as_view(), name='listarPagosProfesor'),
    path('pagar/',pagar,name='pagar'),
    path('pagarProfesor/',pagar_profesor,name='pagarProfesor'),

    #--------------------------------CLASES---------------------------------------------
    path('marcarAsistencia/',marcar_asistencia,name='marcarAsistencia'),

    #path('crearProfesor/', ProfesorCreateView.as_view(), name='crearProfesor'),
    path('modificarProfesor/<int:pk>', ProfesorUpdateView.as_view(), name='modificarProfesor'),
    path('eliminarProfesor/<int:pk>', ProfesorDeleteView.as_view(), name='eliminarProfesor'),
    #path('eliminarProfesor/<int:pk>', profesor_eliminar, name='eliminarProfesor'),
    path('detallarProfesor/<int:pk>', ProfesorDetailView.as_view(), name='detallarProfesor'),
    path('listarProfesores/', ProfesorListView.as_view(), name='listarProfesores'),
    

  
    path('eliminarClase/<int:pk>', ClaseDeleteView.as_view(), name='eliminarClase'),
    path('detallarClase/<int:pk>', ClaseDetailView.as_view(), name='detallarClase'),
    path('listarClases/', ClaseListView.as_view(), name='listarClases'),



    
    path('crearAlumno/', crear_alumno, name='crearAlumno'), 
    path('listarAlumnos/', AlumnoListView.as_view(), name='listarAlumnos'),
    path('detallarAlumno/<int:pk>', AlumnoDetailView.as_view(), name='detallarAlumno'),
    path('modificarAlumno/<int:pk>', AlumnoUpdateView.as_view(), name='modificarAlumno'),
    path('eliminarAlumno/<int:pk>', AlumnoDeleteView.as_view(), name='eliminarAlumno'),

        
]
