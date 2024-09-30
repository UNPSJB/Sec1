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
from django.contrib.auth import views as auth_views
from .forms import LoginForm


urlpatterns = [
    path('administrativo/', administrativo, name= 'administrativo'),
    path('contacto/', contacto, name= 'contacto'),
    path('', home, name= 'home'),
    path('personas/', include('apps.personas.urls')),
    path('listadoPendientes/', listadoDePendientes, name='pendientes'),
    # path('listadoAfiliados/', include('apps.afiliados.urls')),
    # path('listadoSalones/', listadoSalones, name='listadoSalones'),
    # path('listadoAlumnos/', listadoAlumnos, name='listadoAlumnos'),
    # path('listadoAlquileres/', listadoAlquileres, name='listadoAlquileres'),
    # path('listadoCursos/', include('apps.cursos.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),  # Usamos la vista genérica
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('usuario/', usuario),
    path('admin/', admin.site.urls),
    path('registro/', registro, name= 'registro'),
    # path('verAlumno/', verAlumno, name='verAlumno'),
    # path('verAlquiler/', verAlquiler, name='verAlquiler'),
    # path('verProfesor/', verProfesor, name='verProfesor'),
    # path('verCurso/', verCurso, name='verCurso'),
    # path('verSalon/', verSalon, name='verSalon'),
    # path('verAfiliado/', verAfiliado, name='verAfiliado'),
    path('salones/', include('apps.salones.urls')),
    path('afiliados/', include('apps.afiliados.urls')),
    path('cursos/', include('apps.cursos.urls')),
    path("select2/", include("django_select2.urls")),
]
