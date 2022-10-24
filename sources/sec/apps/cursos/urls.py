from django.urls import path
from apps.cursos import views

urlpatterns = [
    path('', views.cursosIndex, name='cursosIndex'),
]