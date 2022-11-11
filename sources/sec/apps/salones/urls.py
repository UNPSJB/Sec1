from django.urls import path
from apps.salones import views
from django.views.generic import TemplateView
from .views import *
from django.contrib import admin

urlpatterns = [

    
    # ----------------- Salones -----------------
    
    path('listadoSalones/', views.listadoSalones, name='listadoSalones'),

    path('crearSalon/', SalonCreateView.as_view(), name='crearSalon'),
    path('modificarSalon/<int:pk>', SalonCreateView.as_view(), name='modificarSalon'),
    #path('eliminarSalon/', DeleteCreateView.as_view(), name='eliminarSalon'),
    path('eliminarSalon/<int:pk>', salon_eliminar, name='eliminarSalon'),
    path('detallarSalon/<int:pk>', SalonDetailView.as_view(), name='detallarSalon'),
    path('listarSalones/', SalonListView.as_view(), name='listarSalones'),

    # ----------------- Alquileres -----------------

    path('crearAlquiler/', AlquilerCreateView.as_view(), name='crearAlquiler'),
    path('modificarAlquiler/<int:pk>', AlquilerUpdateView.as_view(), name='modificarAlquiler'),
    #path('eliminarAlquiler/', DeleteCreateView.as_view(), name='eliminarAlquiler'),
    path('eliminarAlquiler/<int:pk>', salon_eliminar, name='eliminarAlquiler'),
    path('detallarAlquiler/<int:pk>', SalonDetailView.as_view(), name='detallarAlquiler'),
    path('listarAlquileres/', SalonListView.as_view(), name='listarAlquileres'),

    # ----------------- Servicios -----------------

    path('crearServicio/', ServicioCreateView.as_view(), name='crearServicio'),
    #path('modificarServicio/<int:pk>', SalonCreateView.as_view(), name='modificarServicio'),
    #path('eliminarServicio/', DeleteCreateView.as_view(), name='eliminarServicio'),
    #path('eliminarServicio/<int:pk>', salon_eliminar, name='eliminarServicio'),
    #path('detallarServicio/<int:pk>', SalonDetailView.as_view(), name='detallarServicio'),
    #path('listarServicios/', SalonListView.as_view(), name='listarServicios'),
]