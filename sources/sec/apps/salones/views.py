from django.shortcuts import render

# Create your views here.
def listadoSalones(request):
    return render(request, 'listadoSalones.html', {})