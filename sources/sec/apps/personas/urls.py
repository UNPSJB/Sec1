from django.urls import path
from django.views.generic import TemplateView
from apps.afiliados import views
from .views import *

urlpatterns = [

    # ----------------- PERSONAS -----------------

    path('crear/', PersonaCreateView.as_view(), name='crearPersona'),
]

