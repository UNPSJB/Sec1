from django.urls import path
from django.views.generic import TemplateView
from apps.cursos.views.alumnos import *

urlpatterns = [
    #path('', views.listadoAlumnos, name='listadoAlumno'),

    # ----------------- ALUMNO -----------------

    path('crear/', AlumnoCreateView.as_view(), name='crearAlumno'),
]