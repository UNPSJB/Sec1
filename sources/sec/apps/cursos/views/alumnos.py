from django.shortcuts import render
from apps.cursos.forms import *
from apps.cursos.models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
#def listadoAlumnos(request):
#    return render(request, 'listadoAlumno.html', {})

# ---------------------------- Alumno View ------------------------------------ #

class AlumnoCreateView(CreateView):

    model = Alumno
    form_class = AlumnoForm
    # template_name = 'alumno/alumno_form.html' # template del form
    success_url = reverse_lazy('crearAlumno')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar alumno"
        context['ayuda'] = 'crear_alumno.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        alumno_form = self.get_form()
        

        if alumno_form.is_valid():
            alumno = alumno_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Alumno registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, alumno_form.errors)
        return self.form_invalid(form=alumno_form)