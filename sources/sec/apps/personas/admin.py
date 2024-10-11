from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from .models import Persona, Rol

# Register your models here.
admin.site.register(Persona)
admin.site.register(Rol)
#admin.site.register(User)
#admin.site.register(Group)
admin.site.register(Permission)