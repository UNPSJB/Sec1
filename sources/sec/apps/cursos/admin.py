from django.contrib import admin
from .models import (
    Profesor,
    Alumno, 
    Actividad, 
    Dictado
)

# Register your models here.

admin.site.register(Profesor)
admin.site.register(Alumno)
admin.site.register(Actividad)
admin.site.register(Dictado)