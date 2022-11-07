from django.urls import path
from django.views.generic import TemplateView
from apps.afiliados import views
from .views import *

urlpatterns = [

    # ----------------- PERSONAS -----------------

    path('crearPersona/', PersonaCreateView.as_view(), name='crearPersona'),
    path('modificarPersona/', PersonaUpdateView.as_view(), name='modificarPersona'),
    #path('borrarPersona/', PersonaDeleteView.as_view(), name='borrarPersona'),
    path('eliminarPersona/', persona_eliminar, name='eliminarPersona'),
    path('detallarPersona/', PersonaDetailView.as_view(), name='detallarPersona'),
    path('listarPersonas/', PersonaListView.as_view(), name='listarPersonas'),
]

