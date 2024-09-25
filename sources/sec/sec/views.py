from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def administrativo(request):
#    print (request.user.persona)
    return render(request,"administrativo.html")

def beneficios(request):
    return render(request,"beneficios.html")

def contacto(request):
    return render(request,"contacto.html")


def home(request):
    return render(request,"home.html")

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

def listadoDePendientes(request):
    return render(request,"listadoPendientes.html")

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

# def verAfiliado(request):
#     return render(request,"verAfiliado.html")