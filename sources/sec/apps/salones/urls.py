from django.urls import path
from apps.salones import views
from django.views.generic import TemplateView
from .views import *
from django.contrib import admin

urlpatterns = [

    # ----------------- Encargados -----------------
    path('crearEncargado/', crear_persona_y_encargado, name='crearEncargado'),
    path('buscarPersonaEncargado/',buscar_persona_para_encargado,name='buscarPersonaParaEncargado'),

    path('listarEncargados/', EncargadoListView.as_view(), name='listarEncargados'),
    path('modificarEncargado/<int:pk>', EncargadoUpdateView.as_view(), name='modificarEncargado'),
    path('eliminarEncargado/<int:pk>', eliminar_encargado, name='eliminarEncargado'),


    # ----------------- Salones -----------------
    
    path('listadoSalones/', views.listadoSalones, name='listadoSalones'),

    path('crearSalon/', SalonCreateView.as_view(), name='crearSalon'),
    path('modificarSalon/<int:pk>', SalonUpdateView.as_view(), name='modificarSalon'),
    path('eliminarSalon/<int:pk>', SalonDeleteView.as_view(), name='eliminarSalon'),
    #path('eliminarSalon/<int:pk>', salon_eliminar, name='eliminarSalon'),
    path('detallarSalon/<int:pk>', SalonDetailView.as_view(), name='detallarSalon'),
    path('listarSalones/', SalonListView.as_view(), name='listarSalones'),
    path('cambiarEstadoSalon/', views.cambiar_estado_salon, name='cambiarEstadoSalon'),


    # ----------------- Alquileres -----------------

    path('crearAlquiler/', AlquilerCreateView.as_view(), name='crearAlquiler'),
    path('crearAlquiler/<int:salon_pk>', AlquilerCreateView.as_view(), name='crearAlquilerSalon'),
    path('modificarAlquiler/<int:pk>', AlquilerUpdateView.as_view(), name='modificarAlquiler'),
    path('eliminarAlquiler/<int:pk>', AlquilerDeleteView.as_view(), name='eliminarAlquiler'),
    path('detallarAlquiler/<int:pk>', AlquilerDetailView.as_view(), name='detallarAlquiler'),
    path('listarAlquileres/', AlquilerListView.as_view(), name='listarAlquileres'),
    path('registrar_pago/<int:pago_id>', registrar_pago, name='registrar_pago'),
    path('crear_cuotas/<int:alquiler_id>/', crear_cuotas, name='crear_cuotas'),
    path('pagar_senia/<int:alquiler_id>/', pagar_senia, name='pagar_senia'),
    path('reemplazar_alquiler/<int:alquiler_id>/', reemplazar_alquiler, name='reemplazar_alquiler'),
    path('salon/<int:salon_pk>/lista_espera/<str:inicio>/', ListaEsperaView.as_view(), name='lista_espera'),
    path('alquiler/<int:alquiler_id>/cuotas/', PagoAlquilerListView.as_view(), name='listar_cuotas'),
    path('buscar_afiliado/', buscar_afiliado, name='buscar_afiliado'),
    path('obtener_dias_ocupados/<int:salon_pk>/', obtener_dias_ocupados, name='obtener_dias_ocupados'),

    # ----------------- Servicios -----------------

    path('crearServicio/', ServicioCreateView.as_view(), name='crearServicio'),
    path('modificarServicio/<int:pk>', views.modificarServicio, name='modificarServicio'),
    path('eliminarServicio/<int:pk>', ServicioDeleteView.as_view(), name='eliminarServicio'),
    #path('eliminarServicio/<int:pk>', servicio_eliminar, name='eliminarServicio'),
    path('detallarServicio/<int:pk>', ServicioDetailView.as_view(), name='detallarServicio'),
    path('listarServicios/', ServicioListView.as_view(), name='listarServicios'),
    path('cambiarEstadoServicio/', views.cambiar_estado, name='cambiarEstadoServicio'),


]