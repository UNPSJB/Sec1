from django.contrib import admin
#from django.contrib.auth.models import User, Group, Permission
from .models import Salon, Alquiler

class SalonInLine(admin.TabularInline):
    model = Salon
    fk_name = "salon"

class AlquilerInline(admin.TabularInline):
    model = Alquiler
    fk_name = "alquiler"

#class PersonaAdmin(admin.ModelAdmin):
#    model = Persona
#    inlines = [
#        VinculoInline,
#    ]

# Register your models here.
#admin.site.register(Persona, PersonaAdmin)
admin.site.register(Salon)
admin.site.register(Alquiler)
#admin.site.register(User)
#admin.site.register(Group)
#admin.site.register(Permission)
