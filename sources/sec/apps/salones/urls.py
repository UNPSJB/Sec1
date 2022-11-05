from django.urls import path
from apps.salones import views
from django.views.generic import TemplateView
from .views import *

urlpatterns = [

    path('', views.listadoSalones, name='listadoSalones'),
    # ----------------- Salones -----------------

    path('crear/', SalonCreateView.as_view(), name='crearSalon'),
]