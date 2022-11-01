from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from .models import Persona

# Register your models here.
admin.site.register(Persona)
#admin.site.register(User)
#admin.site.register(Group)
admin.site.register(Permission)