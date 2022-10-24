from django.urls import path
from apps.salones import views

urlpatterns = [
    path('', views.listadoSalones, name='listadoSalones'),
]