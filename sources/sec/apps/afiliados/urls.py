from django.urls import path
from django.views.generic import TemplateView
from apps.afiliados import views
from .views import *

urlpatterns = [
    path('', views.listadoAfiliados, name='listadoAfiliados'),

    # ----------------- AFILIADOS -----------------

    #path('clientes/listar', AfiliadoListView.as_view(), name='listarClientes'),
    path('crear/', AfiliadoCreateView.as_view(), name='crearAfiliado')
]