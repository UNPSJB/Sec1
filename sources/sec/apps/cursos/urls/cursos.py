from django.urls import path
from apps.cursos.views import cursos

urlpatterns = [
    path('', cursos.listadoCursos, name='listadoCursos'),
    path('index', cursos.cursosIndex, name='cursosIndex'),
]