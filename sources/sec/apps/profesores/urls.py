from django.urls import path
from apps.profesores import views

urlpatterns = [
    path('', views.listadoProfesores, name='listadoProfesores'),
]