from django.contrib import admin
from .models import (
    Profesor, 
    Especialidad, 
    Alumno, 
    Curso, 
    Titularidad, 
    Dictado
)

# Register your models here.

admin.site.register(Profesor)
admin.site.register(Alumno)
admin.site.register(Curso)
admin.site.register(Especialidad)
admin.site.register(Titularidad)
admin.site.register(Dictado)