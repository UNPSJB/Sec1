from django.shortcuts import render

# Create your views here.
def listadoAfiliados(request):
    return render(request, 'listadoAfiliados.html', {})