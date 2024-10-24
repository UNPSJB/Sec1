
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



def staff_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))  
    return _wrapped_view
