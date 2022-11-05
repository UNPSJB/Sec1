from django.urls import path
from .views import *
from apps.cursos import views 

urlpatterns = [
    #path('', views.listadoProfesores, name='listadoProfesores'),
    #path('index', cursos.cursosIndex, name='cursosIndex'),
    path('crearProfesor/', ProfesorCreateView.as_view(), name='crearProfesor'),

    #path('', views.listadoCursos, name='listadoCursos'),
    #path('index', cursos.cursosIndex, name='cursosIndex'),
    path('crearCurso/', CursoCreateView.as_view(), name='crearCurso'),
    
    #path('', views.listadoAlumnos, name='listadoAlumnos'),
    #path('index', cursos.cursosIndex, name='cursosIndex'),
    path('crearAlumno/', AlumnoCreateView.as_view(), name='crearAlumno'), 

    #path('', views.listadoClases, name='listadoClases'),
    #path('index', clases.clasesIndex, name='clasesIndex'),
    path('crearClase/', ClaseCreateView.as_view(), name='crearClase'),

    #path('', views.listadoAulas, name='listadoAulas'),
    #path('index', clases.clasesIndex, name='clasesIndex'),
    path('crearAula/', AulaCreateView.as_view(), name='crearAula'),               
]
