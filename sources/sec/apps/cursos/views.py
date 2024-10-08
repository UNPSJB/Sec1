from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

#--------------------------------PROFESOR---------------------------------------------

class ProfesorCreateView(CreateView):

    model = Profesor
    form_class = CrearProfesorForm

    def get_success_url(self):
        return reverse_lazy('detallarProfesor', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Profesor registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
 
class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = ModificarProfesorForm

    def get_success_url(self):
        return reverse_lazy('detallarProfesor', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Profesor"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Profesor modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

def profesor_eliminar(request, pk):
    a = Profesor.objects.get(pk=pk)
    a.delete()
    return redirect('listarProfesores') 

class ProfesorDeleteView(DeleteView):
    model = Profesor
    success_url = reverse_lazy('listarProfesores')

class ProfesorDetailView(DetailView):
    model = Profesor

class ProfesorListView(ListView):
    model = Profesor
    paginate_by = 100 

#--------------------------------ALUMNO-----------------------------------------------

class AlumnoCreateView(CreateView):

    model = Alumno
    form_class = CrearAlumnoForm

    def get_success_url(self):
        return reverse_lazy('detallarAlumno', kwargs={'pk': self.object.pk})

    #def get_initial(self):
        # Validar dni de entrada
    #    p = Persona.objects.filter(dni=self.request.GET["dni"]).first()
    #    return {"dni": p.dni}
     
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Alumno registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class AlumnoListView(ListView):
    model = Alumno
    paginate_by = 100 

class AlumnoDetailView(DetailView):
    model = Alumno

class AlumnoDeleteView(DeleteView):
    model = Alumno
    success_url = reverse_lazy('listarAlumnos')

class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = ModificarAlumnoForm

    def get_success_url(self):
        return reverse_lazy('detallarAlumno', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Alumnooo"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Alumno modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

def alumno_agregar_dictado(request, apk, dpk):
    alumno = Alumno.objects.get(pk=apk)
    dictado = Dictado.objects.get(pk=dpk)
    alumno.inscribirADictado(dictado)
    return redirect('detallarDictado', dpk) #elegir a donde ir (?

def alumno_bajar_dictado(request, apk, dpk):
    alumno = Alumno.objects.get(pk=apk)
    alumno.desinscribiDeDictado()
    return redirect('detallarDictado', dpk) #elegir a donde ir (?

#--------------------------------CURSO---------------------------------------------

class CursoCreateView(CreateView):

    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('listarCursos')

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy("listarCursos")

def curso_eliminar(request, pk):
    a = Curso.objects.get(pk=pk)
    a.delete()
    return redirect('listarCursos') 

class CursoDeleteView(DeleteView):
    model = Curso
    success_url = reverse_lazy('listarCursos')

class CursoDetailView(DetailView):
    model = Curso

class CursoListView(ListView):
    model = Curso
    paginate_by = 100 

def listadoCursos(request):
    return render(request, 'listadoCursos.html', {})


#--------------------------------AULA---------------------------------------------

class AulaCreateView(CreateView):

    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('listarAulas')

class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy("listarAulas")

#def aula_eliminar(request, pk):
#   a = Aula.objects.get(pk=pk)
#   a.delete()
#   return redirect('listarAulas') 

class AulaDeleteView(DeleteView):
    model = Aula
    success_url = reverse_lazy('listarAulas')

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

class EspecialidadDeleteView(DeleteView):
    model = Especialidad
    success_url = reverse_lazy('listarEspecialidades')

class EspecialidadDetailView(DetailView):
    model = Especialidad

class EspecialidadListView(ListView):
    model = Especialidad
    paginate_by = 100 

#--------------------------------DICTADO---------------------------------------------
class DictadoCreateView(CreateView):

    model = Dictado
    form_class = CrearDictadoForm
    success_url = reverse_lazy('listarDictados')

    def get_initial(self):
        curso = get_object_or_404(Curso, pk=self.kwargs.get('pk', 0))
        initial = super().get_initial()
        initial["curso"] = curso
        return initial

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Dictado registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

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

def dictado_iniciar(request, pk):
    dictado = Dictado.objects.get(pk=pk)
    curso = dictado.curso
    alumnos = curso.alumnos.all().filter(dictado=None)
    context = {'dictado': dictado,'curso': curso, 'alumnos': alumnos}
    return render(request, 'cursos/dictado_iniciar.html' , context)

class DictadoDeleteView(DeleteView):
    model = Dictado
    success_url = reverse_lazy('listarDictados')

class DictadoDetailView(DetailView):
    model = Dictado

class DictadoListView(ListView):
    model = Dictado
    paginate_by = 100 
 

# def listadoDictados(request):
#     return render(request, 'listadoDictados.html', {})

#--------------------------------CLASE---------------------------------------------
class ClaseCreateView(CreateView):

    model = Clase
    form_class = ClaseForm
    success_url = reverse_lazy('listarClases')

    def get_success_url(self):
        return reverse_lazy('detallarDictado', kwargs={'pk': self.object.dictado.pk})

    def get_initial(self):
        dictado = get_object_or_404(Dictado, pk=self.kwargs.get('pk', 0))
        initial = super().get_initial()
        initial["dictado"] = dictado
        return initial

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Clase registrada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class ClaseUpdateView(UpdateView):
    model = Clase
    form_class = ClaseForm
    success_url = reverse_lazy("listarClases")
"""
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Clase modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
"""
def clase_eliminar(request, pk):
    a = Clase.objects.get(pk=pk)
    a.delete()
    return redirect('listarClases') 

class ClaseDeleteView(DeleteView):
    model = Clase
    success_url = reverse_lazy('listarClases')

class ClaseDetailView(DetailView):
    model = Clase

class ClaseListView(ListView):
    model = Clase
    paginate_by = 100 

#--------------------------------PAGO DICTADO---------------------------------------------
class PagoDictadoCreateView(CreateView):

    model = PagoDictado
    form_class = PagoDictadoForm
    success_url = reverse_lazy('listarPagosDictados')

    def get_initial(self):
        dictado = get_object_or_404(Dictado, pk=self.kwargs.get('cpk', 0))
        initial = super().get_initial()
        initial["dictado"] = dictado
        return initial

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Pago de Dictado registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class PagoDictadoUpdateView(UpdateView):
    model = PagoDictado
    form_class = PagoDictadoForm
    success_url = reverse_lazy("listarPagosDictados")
"""
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Dictado modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
"""
def pago_dictado_eliminar(request, pk):
    a = PagoDictado.objects.get(pk=pk)
    a.delete()
    return redirect('listarPagosDictados') 

class PagoDictadoDeleteView(DeleteView):
    model = PagoDictado
    success_url = reverse_lazy('listarPagosDictados')

class PagoDictadoDetailView(DetailView):
    model = PagoDictado

class PagoDictadoListView(ListView):
    model = PagoDictado
    paginate_by = 100 