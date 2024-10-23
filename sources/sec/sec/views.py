from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def staff_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))  
    return _wrapped_view


@staff_required
def administrativo(request):
#    print (request.user.persona)
    return render(request,"administrativo.html")


def contacto(request):
    return render(request,"contacto.html")


def home(request):
    return redirect("login")

# def listadoCursos(request):
#     return render(request,"listadoCursos.html")

# def listadoSalones(request):
#     return render(request,"listadoSalones.html")

def login(request):
    return render(request,"login.html")


def usuario(request):
    return render(request,"usuario.html")

def registro(request):
    return render(request, "registro.html")

# def listadoAlquileres(request):
#     return render(request,"listadoAlquileres.html")

# def listadoAlumnos(request):
#     return render(request,"listadoAlumnos.html")

# def verAlumno(request):
#     return render(request,"verAlumno.html")

# def verAlquiler(request):
#     return render(request,"verAlquiler.html")

# def verProfesor(request):
#     return render(request,"verProfesor.html")

# def verCurso(request):
#     return render(request,"verCurso.html")

# def verSalon(request):
#     return render(request,"verSalon.html")