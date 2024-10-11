from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from .models import Persona, Rol

""" class VinculoInline(admin.TabularInline):
    model = Vinculo
    fk_name = "vinculante"

class PersonaAdmin(admin.ModelAdmin):
    model = Persona
    inlines = [
        VinculoInline,
    ] """

# Register your models here.
admin.site.register(Persona)
admin.site.register(Rol)
#admin.site.register(User)
#admin.site.register(Group)
admin.site.register(Permission)