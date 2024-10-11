from django.urls import path
from django.views.generic import TemplateView
from apps.afiliados import views
from .views import *


urlpatterns = [
    # ----------------- AFILIADOS -----------------
    path('crearAfiliado/', crear_persona_y_afiliado, name='crearAfiliado'),
    path('buscarPersonaAfiliado/',buscar_persona_para_afiliado,name='buscarPersonaParaAfiliado'),
    path('aceptar/<int:afiliado_id>', aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar/', rechazar_solicitud, name='rechazar_solicitud'),
    path('desafiliar/', desafiliar, name='desafiliar'),
    path('modificarAfiliado/<int:pk>', AfiliadoUpdateView.as_view(), name='modificarAfiliado'),
    path('detallarAfiliado/<int:pk>', AfiliadoDetailView.as_view(), name='detallarAfiliado'),
    path('listarAfiliados/', AfiliadoListView.as_view(), name='listarAfiliados'),
    path('afiliacionesPendientes/', AfiliacionesPendientes.as_view(), name='afiliacionesPendientes'),
    path('detallarSolicitud/<int:pk>', AfiliacionPendienteDetailView.as_view(), name='detallarSolicitud'),

    # ----------------- FAMILIAR -----------------
    path('buscarPersonaFamiliar/',buscar_persona_para_familiar,name='buscarPersonaParaFamiliar'),
    path('crearFamiliar/', crear_familiar, name='crear_familiar'),
    path('quitarFamiliar/', quitarFamiliar, name='quitarFamiliar'),

    # ----------------- COMERCIOS -----------------
    path('buscarComercio/', buscar_comercio, name='buscar_comercio'),
    path('crearComercio/', crear_comercio, name='crear_comercio'),
]