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
    return render(request,"administrativo.html")

def home(request):
    return redirect("login")

def login(request):
    return render(request,"login.html")
