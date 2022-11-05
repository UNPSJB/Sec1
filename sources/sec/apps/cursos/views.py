from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

#--------------------------------PROFESOR---------------------------------------------

class ProfesorCreateView(CreateView):

    model = Profesor
    form_class = ProfesorForm
    # template_name = 'profesores/profesor_form.html' # template del form
    success_url = reverse_lazy('crearProfesor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar profesor"
        context['ayuda'] = 'crear_profesor.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        profesor_form = self.get_form()
        

        if profesor_form.is_valid():
            profesor = profesor_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Profesor registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, profesor_form.errors)
        return self.form_invalid(form=profesor_form)

#--------------------------------ALUMNO-----------------------------------------------

class AlumnoCreateView(CreateView):

    model = Alumno
    form_class = AlumnoForm
    # template_name = 'alumnos/alumno_form.html' # template del form
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

#--------------------------------CURSO---------------------------------------------

class CursoCreateView(CreateView):

    model = Curso
    form_class = CursoForm
    # template_name = 'cursos/curso_form.html' # template del form
    success_url = reverse_lazy('crearCurso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar curso"
        context['ayuda'] = 'crear_curso.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        curso_form = self.get_form()
        

        if curso_form.is_valid():
            curso = curso_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Curso registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, curso_form.errors)
        return self.form_invalid(form=curso_form)

#--------------------------------CLASE---------------------------------------------

class ClaseCreateView(CreateView):

    model = Clase
    form_class = ClaseForm
    # template_name = 'clases/clase_form.html' # template del form
    success_url = reverse_lazy('crearClase')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar clase"
        context['ayuda'] = 'crear_clase.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        clase_form = self.get_form()
        

        if clase_form.is_valid():
            clase = clase_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Clase registrada con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, clase_form.errors)
        return self.form_invalid(form=clase_form)

#--------------------------------AULA---------------------------------------------

class AulaCreateView(CreateView):

    model = Aula
    form_class = AulaForm
    # template_name = 'aulas/aula_form.html' # template del form
    success_url = reverse_lazy('crearAula')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar aula"
        context['ayuda'] = 'crear_aula.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        aula_form = self.get_form()
        

        if aula_form.is_valid():
            aula = aula_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Aula registrada con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, aula_form.errors)
        return self.form_invalid(form=aula_form)