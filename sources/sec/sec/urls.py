"""sec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('administrativo/', administrativo, name= 'administrativo'),
    path('beneficios/', beneficios),
    path('contacto/', contacto, name= 'contacto'),
    #path('cursos.html/', cursos),
    path('cursos/', include('apps.cursos.urls.cursos')),
    path('gimnasio/', gimnasio),
    path('', home, name= 'home'),
    #path('listadoAfiliados.html/', listadoAfiliados, ),
    path('listadoPendientes/', listadoDePendientes, name='pendientes'),
    path('listadoAfiliados/', include('apps.afiliados.urls')),
    path('agregarCurso/', agregarCurso, name='agregarCurso'),
    path('listadoCursos/', listadoCursos, name='listadoCursos'),
    path('agregarProfesor/', agregarProfesor, name='agregarProfesor'),
    path('agregarAfiliado/', agregarAfiliado, name='agregarAfiliado'),
    #path('listadoProfesores/', listadoProfesores, name='listadoProfesores'),
    path('agregarSalon/', agregarSalon, name='agregarSalon'),
    path('listadoSalones/', listadoSalones, name='listadoSalones'),
    path('agregarAlumno/', agregarAlumno, name='agregarAlumno'),
    path('listadoAlumnos/', listadoAlumnos, name='listadoAlumnos'),
    path('agregarAlquiler/', agregarAlquiler, name='agregarAlquiler'),
    path('listadoAlquileres/', listadoAlquileres, name='listadoAlquileres'),
    path('listadoCursos/', include('apps.cursos.urls.cursos')),
    path('listadoProfesores/', include('apps.cursos.urls.profesores')),
    path('listadoSalones/', include('apps.salones.urls')),
    path('login/', login, name= 'login'),
    path('usuario/', usuario),
    path('admin/', admin.site.urls),
    path('registro/', registro, name= 'registro'),
<<<<<<< HEAD
    path('afiliados/', include('apps.afiliados.urls'))
=======
    path('verAlumno/', verAlumno, name='verAlumno'),
    path('verAlquiler/', verAlquiler, name='verAlquiler'),
    path('verProfesor/', verProfesor, name='verProfesor'),
    path('verCurso/', verCurso, name='verCurso'),
    path('verSalon/', verSalon, name='verSalon'),
    path('verAfiliado/', verAfiliado, name='verAfiliado'),
>>>>>>> 02a1b23849bbfacd16958d25522f0b7e4affce13
]
