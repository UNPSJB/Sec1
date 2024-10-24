from django.shortcuts import render
from sec.decorators import staff_required
from django.shortcuts import redirect


@staff_required
def administrativo(request):
    return render(request,"administrativo.html")

def home(request):
    return redirect("login")

def login(request):
    return render(request,"login.html")
