from django.shortcuts import render

def administrativo(request):
    return render(request,"administrativo.html")

def beneficios(request):
    return render(request,"beneficios.html")

def contacto(request):
    return render(request,"contacto.html")

#def cursos(request):
#    return render(request,"cursos.html")

def gimnasio(request):
    return render(request,"gimnasio.html")

def home(request):
    return render(request,"home.html")

#def listadoAfiliados(request):
#    return render(request,"listadoAfiliados.html")

#def listadoCursos(request):
#    return render(request,"listadoCursos.html")

#def listadoProfesores(request):
#    return render(request,"listadoProfesores.html")

def listadoSalones(request):
    return render(request,"listadoSalones.html")

def login(request):
    return render(request,"login.html")

def usuario(request):
    return render(request,"usuario.html")

