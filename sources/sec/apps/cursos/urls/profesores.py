from django.urls import path
from apps.cursos.views import profesores

urlpatterns = [
    path('', profesores.listadoProfesores, name='listadoProfesores'),
]