from django.shortcuts import render

# Create your views here.
def listadoProfesores(request):
    return render(request, 'listadoProfesores.html', {})