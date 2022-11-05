from django.urls import path
from apps.salones import views
from django.views.generic import TemplateView
from .views import *

urlpatterns = [

    
    # ----------------- Salones -----------------
    
    path('', views.listadoSalones, name='listadoSalones'),
    path('crearSalon/', SalonCreateView.as_view(), name='crearSalon'),

    # ----------------- Alquileres -----------------

    path('crearAlquiler/', AlquilerCreateView.as_view(), name='crearAlquiler'),

    # ----------------- Servicios -----------------

    path('crearServicio/', ServicioCreateView.as_view(), name='crearServicio'),
]