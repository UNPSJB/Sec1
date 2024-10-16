from django.urls import path
from apps.salones import views
from django.views.generic import TemplateView
from .views import *
from django.contrib import admin

urlpatterns = [

    # ----------------- Encargados -----------------
    path('crearEncargado/', EncargadoCreateView.as_view(), name='crearEncargado'),
    path('listarEncargados/', EncargadoListView.as_view(), name='listarEncargados'),


    # ----------------- Salones -----------------
    
    path('listadoSalones/', views.listadoSalones, name='listadoSalones'),

    path('crearSalon/', SalonCreateView.as_view(), name='crearSalon'),
    path('modificarSalon/<int:pk>', SalonCreateView.as_view(), name='modificarSalon'),
    path('eliminarSalon/<int:pk>', SalonDeleteView.as_view(), name='eliminarSalon'),
    #path('eliminarSalon/<int:pk>', salon_eliminar, name='eliminarSalon'),
    path('detallarSalon/<int:pk>', SalonDetailView.as_view(), name='detallarSalon'),
    path('listarSalones/', SalonListView.as_view(), name='listarSalones'),

    # ----------------- Alquileres -----------------

    path('crearAlquiler/', AlquilerCreateView.as_view(), name='crearAlquiler'),
    path('crearAlquiler/<int:salon_pk>', AlquilerCreateView.as_view(), name='crearAlquilerSalon'),
    path('modificarAlquiler/<int:pk>', AlquilerUpdateView.as_view(), name='modificarAlquiler'),
    path('eliminarAlquiler/', AlquilerDeleteView.as_view(), name='eliminarAlquiler'),
    #path('eliminarAlquiler/<int:pk>', alquiler_eliminar, name='eliminarAlquiler'),
    path('detallarAlquiler/<int:pk>', AlquilerDetailView.as_view(), name='detallarAlquiler'),
    path('listarAlquileres/', AlquilerListView.as_view(), name='listarAlquileres'),
    path('comprobante_senia/<int:pk>/', comprobante_senia, name='comprobante_senia'),
    path('elegir_forma_pago/<int:pk>/', elegir_forma_pago, name='elegir_forma_pago'),
    path('pago_unico/<int:pk>/', pago_unico, name='pago_unico'),

    # ----------------- Servicios -----------------

    path('crearServicio/', ServicioCreateView.as_view(), name='crearServicio'),
    path('modificarServicio/<int:pk>', ServicioCreateView.as_view(), name='modificarServicio'),
    path('eliminarServicio/<int:pk>', ServicioDeleteView.as_view(), name='eliminarServicio'),
    #path('eliminarServicio/<int:pk>', servicio_eliminar, name='eliminarServicio'),
    path('detallarServicio/<int:pk>', ServicioDetailView.as_view(), name='detallarServicio'),
    path('listarServicios/', ServicioListView.as_view(), name='listarServicios'),
]