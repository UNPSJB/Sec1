from django.urls import path
from apps.afiliados import views

urlpatterns = [
    path('', views.listadoAfiliados, name='listadoAfiliados'),
]