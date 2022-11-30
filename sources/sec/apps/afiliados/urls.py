from django.urls import path
from django.views.generic import TemplateView
from apps.afiliados import views
from .views import *

urlpatterns = [
    path('', views.listadoAfiliados, name='listadoAfiliados'),

    # ----------------- AFILIADOS -----------------

    path('crearAfiliado/', AfiliadoCreateView.as_view(), name='crearAfiliado'),
    path('modificarAfiliado/<int:pk>', AfiliadoUpdateView.as_view(), name='modificarAfiliado'),
    path('eliminarAfiliado/<int:pk>/', AfiliadoDeleteView.as_view(), name='eliminarAfiliado'),
    #path('eliminarAfiliado/<int:pk>/', afiliado_eliminar, name='eliminarAfiliado'),
    path('detallarAfiliado/<int:pk>', AfiliadoDetailView.as_view(), name='detallarAfiliado'),
    path('listarAfiliados/', AfiliadoListView.as_view(), name='listarAfiliados'),
]