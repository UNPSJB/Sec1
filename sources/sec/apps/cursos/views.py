from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

#--------------------------------PROFESOR---------------------------------------------

class ProfesorCreateView(CreateView):

    model = Profesor
    form_class = CrearProfesorForm
    # template_name = 'profesores/profesor_form.html' # template del form
    success_url = reverse_lazy('listarProfesores')
"""

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
"""
class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = CrearProfesorForm
    success_url = reverse_lazy("listarProfesores")
"""
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Profesor modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
"""
def profesor_eliminar(request, pk):
    a = Profesor.objects.get(pk=pk)
    a.delete()
    return redirect('listarProfesores') 

#class ProfesorDeleteView(DeleteView):
#    model = Profesor
#    success_url = reverse_lazy('listarProfesores')

class ProfesorDetailView(DetailView):
    model = Profesor

class ProfesorListView(ListView):
    model = Profesor
    paginate_by = 100 

#--------------------------------ALUMNO-----------------------------------------------

class AlumnoCreateView(CreateView):

    model = Alumno
    form_class = CrearAlumnoForm
    # template_name = 'alumnos/alumno_form.html' # template del form
    success_url = reverse_lazy('listarAlumnos')

    #def get_initial(self):
        # Validar dni de entrada
    #    p = Persona.objects.filter(dni=self.request.GET["dni"]).first()
    #    return {"dni": p.dni}
     
    def post(self, *args, **kwargs):
        self.object = None
        form = self.get_form() # equivalente a cargaAlumnoForm(self.request.POST)
        if form.is_valid(): # este is_valid() llama internamente al is_valid() de los forms que lo componen.
            alumno = form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Alumno registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarAlumnos')
            return redirect('listarAlumnos')
        else:
            print("Errores", form.errors)
            messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form=form)

class AlumnoListView(ListView):
    model = Alumno
    paginate_by = 100 

class AlumnoDetailView(DetailView):
    model = Alumno

class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = CrearAlumnoForm
    success_url = reverse_lazy("listarAlumnos")

#--------------------------------CURSO---------------------------------------------

class CursoCreateView(CreateView):

    model = Curso
    form_class = CursoForm
    # template_name = 'cursos/curso_form.html' # template del form
    success_url = reverse_lazy('listarCursos')
"""

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
"""

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy("listarCursos")

def curso_eliminar(request, pk):
    a = Curso.objects.get(pk=pk)
    a.delete()
    return redirect('listarCursos') 

#class CursoDeleteView(DeleteView):
#    model = Curso
#    success_url = reverse_lazy('listarCursos')

class CursoDetailView(DetailView):
    model = Curso

class CursoListView(ListView):
    model = Curso
    paginate_by = 100 

def listadoCursos(request):
    return render(request, 'listadoCursos.html', {})
#--------------------------------CLASE---------------------------------------------

class ClaseCreateView(CreateView):

    model = Clase
    form_class = ClaseForm
    # template_name = 'clases/clase_form.html' # template del form
    success_url = reverse_lazy('listarClases')


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
    success_url = reverse_lazy('listarAulas')
"""
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

"""

class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy("listarAulas")

def aula_eliminar(request, pk):
    a = Aula.objects.get(pk=pk)
    a.delete()
    return redirect('listarAulas') 

#class AulaDeleteView(DeleteView):
#    model = Aula
#    success_url = reverse_lazy('listarAulas')

class AulaDetailView(DetailView):
    model = Aula

class AulaListView(ListView):
    model = Aula
    paginate_by = 100 

#--------------------------------ESPECIALIDAD---------------------------------------------

class EspecialidadCreateView(CreateView):

    model = Especialidad
    form_class = EspecialidadForm
    # template_name = 'especialidades/especialidad_form.html' # template del form
    success_url = reverse_lazy('listarEspecialidades')

    """
    def post(self, *args, **kwargs):
        self.object = None
        especialidad_form = self.get_form()
        

        if especialidad_form.is_valid():
            especialidad = especialidad_form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Especialidad registrada con éxito')
            if 'guardar' in self.request.POST:
                return redirect('crearEspecialidad')
            return redirect('crearEspecialidad')
        #messages.add_message(self.request, messages.ERROR, 'Error al registrar especialidad ')
        return self.form_invalid(form=especialidad_form)
    """
class EspecialidadUpdateView(UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    success_url = reverse_lazy("listarEspecialidades")
"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Especialidad"
        return context
    
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Persona modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
"""
def especialidad_eliminar(request, pk):
    a = Especialidad.objects.get(pk=pk)
    a.delete()
    return redirect('listarEspecialidades') 

#class EspecialidadDeleteView(DeleteView):
#    model = Especialidad
#    success_url = reverse_lazy('')

class EspecialidadDetailView(DetailView):
    model = Especialidad

class EspecialidadListView(ListView):
    model = Especialidad
    paginate_by = 100 


class DictadoCreateView(CreateView):

    model = Dictado
    form_class = CrearDictadoForm
    success_url = reverse_lazy('listarDictados')

    def post(self, *args, **kwargs):
        self.object = None
        dictado_form = self.get_form()
        if dictado_form.is_valid():
            dictado = dictado_form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Dictado registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarDictados')
            return redirect('listarDictados')
        else:
            print("Errores", dictado_form.errors)
            messages.add_message(self.request, messages.ERROR, dictado_form.errors)
        return self.form_invalid(form=dictado_form)

class DictadoUpdateView(UpdateView):
    model = Dictado
    form_class = DictadoForm
    success_url = reverse_lazy("listarDictados")
"""
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Dictado modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
"""
def dictado_eliminar(request, pk):
    a = Dictado.objects.get(pk=pk)
    a.delete()
    return redirect('listarDictados') 

#class DictadoDeleteView(DeleteView):
#    model = Dictado
#    success_url = reverse_lazy('listarDictados')

class DictadoDetailView(DetailView):
    model = Dictado

class DictadoListView(ListView):
    model = Dictado
    paginate_by = 100 