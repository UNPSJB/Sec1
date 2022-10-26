from django.shortcuts import render

# Create your views here.
def cursosIndex(request):
    return render(request, 'cursos.html', {})

def listadoCursos(request):
    return render(request, 'listadoCursos.html', {})
    