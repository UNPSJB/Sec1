from django.urls import path
from .views import *
from apps.cursos import views 
from django.contrib import admin

urlpatterns = [
    
    path('crearProfesor/', ProfesorCreateView.as_view(), name='crearProfesor'),
    path('modificarProfesor/<int:pk>', ProfesorUpdateView.as_view(), name='modificarProfesor'),
    path('eliminarProfesor/<int:pk>', ProfesorDeleteView.as_view(), name='eliminarProfesor'),
    #path('eliminarProfesor/<int:pk>', profesor_eliminar, name='eliminarProfesor'),
    path('detallarProfesor/<int:pk>', ProfesorDetailView.as_view(), name='detallarProfesor'),
    path('listarProfesores/', ProfesorListView.as_view(), name='listarProfesores'),
    
    path('crearDictado/<int:pk>', DictadoCreateView.as_view(), name='crearDictado'),
    path('modificarDictado/<int:pk>', DictadoUpdateView.as_view(), name='modificarDictado'),
    path('eliminarDictado/<int:pk>', DictadoDeleteView.as_view(), name='eliminarDictado'),
    #path('eliminarDictado/<int:pk>', dictado_eliminar, name='eliminarDictado'),
    path('detallarDictado/<int:pk>', DictadoDetailView.as_view(), name='detallarDictado'),
    path('listarDictados/', DictadoListView.as_view(), name='listarDictados'),
    path('inscribirDictado/<int:apk>/<int:dpk>', alumno_agregar_dictado, name='inscribirDictado'),
    path('desinscribirDictado/<int:apk>/<int:dpk>', alumno_bajar_dictado, name='desinscribirDictado'),
    #path('iniciarDictado/<int:pk>', dictado_iniciar, name='iniciarDictado'),
    #path('listadoDictados', views.listadoDictados, name='listadoDictados'),

    path('crearClase/<int:pk>', ClaseCreateView.as_view(), name='crearClase'),
    path('modificarClase/<int:pk>', ClaseUpdateView.as_view(), name='modificarClase'),
    path('eliminarClase/<int:pk>', ClaseDeleteView.as_view(), name='eliminarClase'),
    path('detallarClase/<int:pk>', ClaseDetailView.as_view(), name='detallarClase'),
    path('listarClases/', ClaseListView.as_view(), name='listarClases'),

    path('crearPagoDictado/<int:apk>/<int:cpk>', PagoDictadoCreateView.as_view(), name='crearPagoDictado'),
    path('modificarPagoDictado/<int:pk>', PagoDictadoUpdateView.as_view(), name='modificarPagoDictado'),
    path('eliminarPagoDictado/<int:pk>', PagoDictadoDeleteView.as_view(), name='eliminarPagoDictado'),
    #path('eliminarPagoDictado/<int:pk>', pago_dictado_eliminar, name='eliminarPagoDictado'),
    path('detallarPagoDictado/<int:pk>', PagoDictadoDetailView.as_view(), name='detallarPagoDictado'),
    path('listarPagosDictados/', PagoDictadoListView.as_view(), name='listarPagosDictados'),

    path('crearCurso/', CursoCreateView.as_view(), name='crearCurso'),
    path('modificarCurso/<int:pk>', CursoUpdateView.as_view(), name='modificarCurso'),
    path('eliminarCurso/<int:pk>', CursoDeleteView.as_view(), name='eliminarCurso'),
    path('detallarCurso/<int:pk>', CursoDetailView.as_view(), name='detallarCurso'),
    path('listarCursos/', CursoListView.as_view(), name='listarCursos'),
    path('listadoCursos', views.listadoCursos, name='listadoCursos'),
    
    path('crearAlumno/', AlumnoCreateView.as_view(), name='crearAlumno'), 
    path('listarAlumnos/', AlumnoListView.as_view(), name='listarAlumnos'),
    path('detallarAlumno/<int:pk>', AlumnoDetailView.as_view(), name='detallarAlumno'),
    path('modificarAlumno/<int:pk>', AlumnoUpdateView.as_view(), name='modificarAlumno'),
    path('eliminarAlumno/<int:pk>', AlumnoDeleteView.as_view(), name='eliminarAlumno'),

    path('crearAula/', AulaCreateView.as_view(), name='crearAula'),
    path('modificarAula/<int:pk>', AulaUpdateView.as_view(), name='modificarAula'),
    path('eliminarAula/<int:pk>', AulaDeleteView.as_view(), name='eliminarAula'),
    path('detallarAula/<int:pk>', AulaDetailView.as_view(), name='detallarAula'),
    path('listarAulas/', AulaListView.as_view(), name='listarAulas'), 

    path('crearEspecialidad/', EspecialidadCreateView.as_view(), name='crearEspecialidad'),
    path('modificarEspecialidad/<int:pk>', EspecialidadUpdateView.as_view(), name='modificarEspecialidad'),
    path('eliminarEspecialidad/<int:pk>', EspecialidadDeleteView.as_view(), name='eliminarEspecialidad'),
    #path('eliminarEspecialidad/<int:pk>', especialidad_eliminar, name='eliminarEspecialidad'),
    path('detallarEspecialidad/<int:pk>', EspecialidadDetailView.as_view(), name='detallarEspecialidad'),
    path('listarEspecialidades/', EspecialidadListView.as_view(), name='listarEspecialidades'),           
]
