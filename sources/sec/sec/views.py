from django.shortcuts import render

def administrativo(request):
    
<<<<<<< HEAD
#    print (request.user.persona)
=======
    #print (request.user.persona)
>>>>>>> 02a1b23849bbfacd16958d25522f0b7e4affce13
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

def agregarCurso(request):
    return render(request,"agregarCurso.html")

def listadoCursos(request):
    return render(request,"listadoCursos.html")
#def listadoCursos(request):
#    return render(request,"listadoCursos.html")

#def listadoProfesores(request):
#    return render(request,"listadoProfesores.html")

def agregarProfesor(request):
    return render(request,"agregarProfesor.html")

def agregarSalon(request):
    return render(request,"agregarSalon.html")

def listadoSalones(request):
    return render(request,"listadoSalones.html")

def login(request):
    return render(request,"login.html")

def usuario(request):
    return render(request,"usuario.html")

def registro(request):
    return render(request, "registro.html")

def listadoAlquileres(request):
    return render(request,"listadoAlquileres.html")

def agregarAlumno(request):
    return render(request,"agregarAlumno.html")

def listadoAlumnos(request):
    return render(request,"listadoAlumnos.html")

def listadoDePendientes(request):
    return render(request,"listadoPendientes.html")

def agregarAfiliado(request):
    return render(request,"agregarAfiliado.html")

def agregarAlquiler(request):
    return render(request,"agregarAlquiler.html")

def verAlumno(request):
    return render(request,"verAlumno.html")

def verAlquiler(request):
    return render(request,"verAlquiler.html")

def verProfesor(request):
    return render(request,"verProfesor.html")

def verCurso(request):
    return render(request,"verCurso.html")

def verSalon(request):
    return render(request,"verSalon.html")

def verAfiliado(request):
    return render(request,"verAfiliado.html")