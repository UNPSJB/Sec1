from django.urls import path
from django.views.generic import TemplateView
from apps.afiliados import views
from .views import *

urlpatterns = [
    path('', views.listadoAfiliados, name='listadoAfiliados'),

    # ----------------- AFILIADOS -----------------

    path('crearAfiliado/', AfiliadoCreateView.as_view(), name='crearAfiliado'),
    path('modificarAfiliado/', AfiliadoUpdateView.as_view(), name='modificarAfiliado'),
    #path('borrarAfiliado/', AfiliadoDeleteView.as_view(), name='borrarAfiliado'),
    path('eliminarAfiliado/', afiliado_eliminar, name='eliminarAfiliado'),
    path('detallarAfiliado/', AfiliadoDetailView.as_view(), name='detallarAfiliado'),
    path('listarAfiliados/', AfiliadoListView.as_view(), name='listarAfiliados'),
]