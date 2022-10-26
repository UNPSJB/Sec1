from django.urls import path
from apps.cursos import views

urlpatterns = [
    path('', views.listadoCursos, name='listadoCursos'),
    path('index', views.cursosIndex, name='cursosIndex'),
]