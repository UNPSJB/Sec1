from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.db.models import Q
from datetime import datetime
from sec.decorators import staff_required
from django.utils.decorators import method_decorator

#--------------------------------ACTIVIDAD---------------------------------------------
class ActividadCreateView(CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividades/actividad_form.html'
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detallarActividad', kwargs={'pk': self.object.pk})

class ActividadUpdateView(UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividades/actividad_form.html'
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detallarActividad', kwargs={'pk': self.object.pk})

class ActividadDetailView(DetailView):
    model = Actividad
    template_name = 'actividades/actividad_detail.html'
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ActividadListView(ListView):
    model = Actividad
    template_name = 'actividades/actividad_list.html'
    paginate_by = 100 
    ordering = 'id'
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@staff_required
def baja_actividad(request):
    if request.method == 'POST':
        actividad_id = request.POST.get('actividad_id')
        actividad = Actividad.objects.get(id=actividad_id)
        actividad.baja()
        messages.success(request, f"Se ha dado de baja la actividad {actividad.nombre}.")
        return redirect(reverse('detallarActividad', args=[actividad.id]))

#--------------------------------DICTADO---------------------------------------------
class DictadoCreateView(CreateView):

    model = Dictado
    form_class = DictadoForm
    success_url = reverse_lazy('listarDictados')
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    """ 
    def get_initial(self):
        curso = get_object_or_404(Curso, pk=self.kwargs.get('pk', 0))
        initial = super().get_initial()
        initial["curso"] = curso
        return initial

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Dictado registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form) """
    def form_invalid(self, form):
        print(form.errors)  # Esto te ayudará a ver qué está fallando
        return super().form_invalid(form)

class DictadoUpdateView(UpdateView):
    model = Dictado
    form_class = DictadoForm
    success_url = reverse_lazy("listarDictados")
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
"""
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Dictado modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
"""

class DictadoDeleteView(DeleteView):
    model = Dictado
    success_url = reverse_lazy('listarDictados')
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class DictadoDetailView(DetailView):
    model = Dictado
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class DictadoListView(ListView):
    model = Dictado
    paginate_by = 100 
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
 

#--------------------------------AULA---------------------------------------------
class AulaCreateView(CreateView):

    model = Aula
    form_class = AulaForm
    #success_url = reverse_lazy('listarAulas')
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # Guarda el objeto
        self.object = form.save()

        # Devuelve una respuesta JSON en lugar de redirigir
        return JsonResponse({
            'success': True,
            'id': self.object.id,
            'message': 'Objeto creado exitosamente.',
        })

    def form_invalid(self, form):
        # Devuelve los errores en formato JSON
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)

class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'cursos/aula_update.html'
    success_url = reverse_lazy("listarAulas")
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AulaDeleteView(DeleteView):
    model = Aula
    success_url = reverse_lazy('listarAulas')
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AulaListView(ListView):
    model = Aula
    paginate_by = 100 
    ordering = 'id'
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

#--------------------------------PROFESOR---------------------------------------------
@staff_required
def buscar_persona_para_profesor(request):
    if request.method == 'POST':
        action = request.POST.get('action')    
        # Primero, verificar si se envió el formulario de DNI
        if action == 'search':
            dni = request.POST.get('dni')
            try:
                # Intenta obtener la persona por el DNI
                persona = Persona.objects.get(dni=dni)
                persona_form = PersonaForm(instance=persona)
                new_action = 'update'
                profesores_existentes = Profesor.objects.filter(persona=persona)
                for profesor_existente in profesores_existentes:
                    if profesor_existente.hasta is None:
                        return JsonResponse({
                            'dni': dni,
                            'profesor_activo': profesor_existente.id,     
                        })
            except Persona.DoesNotExist:
                # Si no existe, crea un nuevo formulario vacío
                persona_form = PersonaForm()
                new_action = 'create'
            # Renderiza el formulario completo con los datos de la persona
            return render(request, 'profesores/crear_profesor_completo.html', {
                'persona_form': persona_form,
                'profesor_form': ProfesorForm(),
                'dni': dni,  # Manten el DNI para uso posterior
                'action': new_action
            })

@staff_required
def crear_profesor(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        # Manejo del formulario completo para guardar
        if action == 'update':
            dni = request.POST.get('dni')
            old_persona = Persona.objects.get(dni=dni)
            persona_form = PersonaForm(request.POST, instance=old_persona)
        else:
            persona_form = PersonaForm(request.POST)

        profesor_form = ProfesorForm(request.POST)

        if persona_form.is_valid() and profesor_form.is_valid():
            persona = persona_form.save()
            profesor = profesor_form.save(commit=False)
            profesor.persona = persona

            # Validación de afiliaciones
            profesores_existentes = Profesor.objects.filter(persona=persona)

            for profesor_existente in profesores_existentes:
                if profesor_existente.hasta is None:
                    messages.error(request, "La persona ya es Profesor")
                    return render(request, 'profesores/crear_profesor.html')

            profesor.save()
            persona.serProfesor()
            messages.success(request, "Profesor registrado exitosamente.")
            return redirect(reverse('detallarProfesor', args=[profesor.id]))
        else:
            # Manejar errores de validación
            for field in persona_form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            for field in profesor_form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            return render(request, 'profesores/crear_profesor.html')

    # Si es un GET inicial, mostrar solo el formulario de DNI
    return render(request, 'profesores/crear_profesor.html')


#--------------------------------INSCRIPCIONES---------------------------------------------
@staff_required
def buscar_alumno(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        try:
            # Intenta obtener la persona por el DNI
            persona = Persona.objects.get(dni=dni)
            alumnos_existentes = Alumno.objects.filter(persona=persona)
            for alumno_existente in alumnos_existentes:
                if alumno_existente.hasta is None:
                    return JsonResponse({
                        'action': 'inscribir',
                        'alumno_id': alumno_existente.id,
                    })

            persona_form = PersonaForm(instance=persona)
            new_action = 'update'
        except Persona.DoesNotExist:
            # Si no existe, crea un nuevo formulario vacío
            persona_form = PersonaForm()
            new_action = 'create'
        # Renderiza el formulario completo con los datos de la persona
        html = render_to_string('alumnos/crear_alumno.html', {
            'persona_form': persona_form,
            'dni': dni,  # Manten el DNI para uso posterior
            'action': new_action
        }, request=request)
        return JsonResponse({
            'action': 'crear',
            'html': html,
        })

@staff_required
def inscripcion_a_dictado(request, dictado_id):
    # Si es un GET inicial, mostrar solo el formulario de DNI
    dictado = Dictado.objects.get(id=dictado_id)
    return render(request, 'inscripciones/inscripcion.html', {
        'dictado': dictado,
        'action': 'inscripcion'
    })

@staff_required
def crear_inscripcion_a_dictado(request):
    if request.method == 'POST':
        inscripcion_form = InscripcionDictadoForm(request.POST)
        if inscripcion_form.is_valid():
            inscripcion = inscripcion_form.save()
            inscripcion.inscribir()
            messages.success(request, "Incripcion realizada exitosamente.")

            redirect_url = reverse('detallarActividad', args=[inscripcion.dictado.actividad.id])
            
            return JsonResponse({
                            'status': 'creado',
                            'redirect_url': redirect_url
                        })
        else:
            # Manejar errores de validación
            for field in inscripcion_form:
                for error in field.errors:
                    print( f"Error en el campo '{field.label}': {error}")
            return JsonResponse({
                            'status': 'nocreado',
                        })
    else:
        action = request.GET.get('action')
        dictado_id = request.GET.get('dictado_id')
        alumno_id = request.GET.get('alumno_id')
        alumno = Alumno.objects.get(id=alumno_id)
        dictado = Dictado.objects.get(id=dictado_id)
        if alumno.esta_inscrito_en_dictado(dictado.id):
            return JsonResponse({
                    'action': 'ya inscripto',
                })

        if action == 'inscripcion':
            monto= dictado.costo
            if alumno.persona.es_afiliado:
                monto = monto-(monto*(int(dictado.actividad.descuento)/100))
            # Si es un GET inicial, mostrar solo el formulario de DNI
            html = render_to_string('inscripciones/comprobante.html', {
                                    'alumno': alumno,
                                    'dictado': dictado,
                                    'pago': monto,
                                    'form': InscripcionDictadoForm(),
                                }, request=request)
        else:
            html = render_to_string('inscripciones/comprobanteColaEspera.html', {
                        'alumno': alumno,
                        'dictado': dictado,
                        'form': InscripcionDictadoForm(),
                    }, request=request)
        return JsonResponse({
                    'action': 'inscribir',
                    'html': html,
                })

@staff_required
def inscripcion_a_clase(request, clase_id):

    # Si es un GET inicial, mostrar solo el formulario de DNI
    clase = Clase.objects.get(id=clase_id)
    return render(request, 'inscripciones/inscripcionClase.html', {
        'clase': clase,
    })

@staff_required
def crear_inscripcion_a_clase(request):
    if request.method == 'POST':
        inscripcion_form = InscripcionClaseForm(request.POST)
        if inscripcion_form.is_valid():
            inscripcion = inscripcion_form.save()
            inscripcion.inscribir_clase()
            messages.success(request, "Incripcion realizada exitosamente.")
            redirect_url = reverse('detallarActividad', args=[inscripcion.clase.dictado.actividad.id])
            return JsonResponse({
                            'status': 'creado',
                            'redirect_url': redirect_url
                        })
        else:
            # Manejar errores de validación
            for field in inscripcion_form:
                for error in field.errors:
                    print( f"Error en el campo '{field.label}': {error}")
            return JsonResponse({
                            'status': 'nocreado',
                        })
    else:
        clase_id = request.GET.get('clase_id')
        alumno_id = request.GET.get('alumno_id')
        alumno = Alumno.objects.get(id=alumno_id)
        clase = Clase.objects.get(id=clase_id)
        if alumno.esta_inscrito_en_clase(clase.id):
            return JsonResponse({
                    'action': 'ya inscripto',
                })

        monto= clase.dictado.costo
        if alumno.persona.es_afiliado:
            monto = monto-(monto*(int(clase.dictado.actividad.descuento)/100))
        # Si es un GET inicial, mostrar solo el formulario de DNI
        html = render_to_string('inscripciones/comprobanteClase.html', {
                                'alumno': alumno,
                                'clase': clase,
                                'pago': monto,
                                'form': InscripcionClaseForm(),
                            }, request=request)
        return JsonResponse({
                    'action': 'inscribir',
                    'html': html,
                })

@staff_required
def inscripcion_a_cola_espera(request, dictado_id):
    # Si es un GET inicial, mostrar solo el formulario de DNI
    dictado = Dictado.objects.get(id=dictado_id)
    return render(request, 'inscripciones/inscripcion.html', {
        'dictado': dictado,
        'action': 'espera'
    })

@staff_required
def crear_inscripcion_a_cola_espera(request):
    if request.method == 'POST':
        inscripcion_form = InscripcionDictadoForm(request.POST)
        if inscripcion_form.is_valid():
            inscripcion = inscripcion_form.save()
            messages.success(request, "Incripcion realizada exitosamente.")
            # Construir la URL de redirección
            redirect_url = reverse('detallarActividad', args=[inscripcion.dictado.actividad.id])
            
            # Retornar la URL en un JSON
            return JsonResponse({'redirect_url': redirect_url})


class InscripcionDetailView(DetailView):
    model = Inscripcion
    template_name = 'inscripciones/inscripcion_detail.html'
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@staff_required
def desinscribir(request):
    if request.method == 'POST':
        inscripcion_id = request.POST.get('inscripcion_id')
        inscripcion = Inscripcion.objects.get(id=inscripcion_id)
        inscripcion.desinscribir()
        messages.success(request, f"Se ha desinscripto a {inscripcion.alumno}.")
        return redirect(reverse('detallarActividad', args=[inscripcion.dictado.actividad.id]))

@staff_required
def inscripcion_desde_espera(request):
    if request.method == 'POST':
        inscripcion_id = request.POST.get('inscripcion_id')
        inscripcion = Inscripcion.objects.get(id=inscripcion_id)
        inscripcion.inscribir()
        messages.success(request, "Incripcion realizada exitosamente.")
        return redirect(reverse('detallarActividad', args=[inscripcion.dictado.actividad.id]))
    else:
        inscripcion_id = request.GET.get('inscripcion_id')
        inscripcion = Inscripcion.objects.get(id=inscripcion_id)

        monto= inscripcion.dictado.costo
        if inscripcion.alumno.persona.es_afiliado:
            monto = monto-(monto*(int(inscripcion.dictado.actividad.descuento)/100))
        # Si es un GET inicial, mostrar solo el formulario de DNI
        return render(request, 'inscripciones/inscripcionDesdeEspera.html', {
                                'alumno': inscripcion.alumno,
                                'dictado': inscripcion.dictado,
                                'pago': monto,
                                'inscripcion_id': inscripcion.id
                            })

#--------------------------------ALUMNO-----------------------------------------------
@staff_required
def crear_alumno(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        # Manejo del formulario completo para guardar
        if action == 'update':
            dni = request.POST.get('dni')
            old_persona = Persona.objects.get(dni=dni)
            persona_form = PersonaForm(request.POST, instance=old_persona)
        else:
            persona_form = PersonaForm(request.POST)

        if persona_form.is_valid():
            persona = persona_form.save(commit=False)
            persona.es_alumno = True
            persona.save()
            Alumno.objects.create(persona=persona)
            return JsonResponse({
                            'status': 'creado',
                        })
        else:
            # Manejar errores de validación
            for field in persona_form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo '{field.label}': {error}")

    # Si es un GET inicial, mostrar solo el formulario de DNI
    return render(request, 'alumnos/crear_alumno.html')




class AlumnoListView(ListView):
    model = Alumno
    paginate_by = 100 
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AlumnoDetailView(DetailView):
    model = Alumno
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AlumnoDeleteView(DeleteView):
    model = Alumno
    success_url = reverse_lazy('listarAlumnos')
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = ModificarAlumnoForm
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

#--------------------------------PAGOS-----------------------------------------------
class PagoListView(ListView):
    model = Pago
    paginate_by = 100 
    template_name = 'pagos/pagos_list.html'
    """ def get_queryset(self):
        # Filtra los pagos de este mes que están pendientes
        return Pago.objects.filter(pago__isnull=True).order_by('id') """
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        # Obtener el mes y el año actuales
        now = datetime.now()
        current_month = now.month
        current_year = now.year

        # Filtrar los pagos que están pendientes (pago is null)
        # y que su fecha sea igual o anterior al mes actual
        return Pago.objects.filter(
            Q(pago__isnull=True) &
            Q(fecha__month__lte=current_month) &
            Q(fecha__year=current_year)
        ).order_by('id')

@staff_required
def pagar(request):
    if request.method == 'POST':
        pago_id = request.POST.get('pago_id')
        pago = Pago.objects.get(id=pago_id)
        pago.pagar()
        messages.success(request, f"Se ha registrado el pago con exito.")
        return redirect(reverse('listarPagos'))


class ProfesorCreateView(CreateView):

    model = Profesor
    form_class = CrearProfesorForm
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

@staff_required
def profesor_eliminar(request, pk):
    a = Profesor.objects.get(pk=pk)
    a.delete()
    return redirect('listarProfesores') 

class ProfesorDeleteView(DeleteView):
    model = Profesor
    success_url = reverse_lazy('listarProfesores')
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProfesorDetailView(DetailView):
    model = Profesor
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProfesorListView(ListView):
    model = Profesor
    paginate_by = 100 



    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



@staff_required
def marcar_asistencia(request):
    if request.method == 'POST':
        clase_id = request.POST.get('clase_id')
        clase = Clase.objects.get(id=clase_id)
        clase.estado = 1
        clase.save()
        messages.success(request, f"Se ha registrado la asistencia.")
        return redirect(reverse('detallarActividad', args=[clase.dictado.actividad.id]))


class LiquidacionListView(ListView):
    model = Liquidacion
    paginate_by = 100 
    template_name = 'pagos/pagos_profesor_list.html'
    """ def get_queryset(self):
        # Filtra los pagos de este mes que están pendientes
        return Pago.objects.filter(pago__isnull=True).order_by('id') """
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        # Obtener el mes y el año actuales
        now = datetime.now()
        current_month = now.month
        current_year = now.year

        # Filtrar los pagos que están pendientes (pago is null)
        # y que su fecha sea igual o anterior al mes actual
        return Liquidacion.objects.filter(
            Q(fechaPago__isnull=True) &
            Q(liquidacion__month__lte=current_month) &
            Q(liquidacion__year=current_year)
        ).order_by('id')

@staff_required
def pagar_profesor(request):
    if request.method == 'POST':
        liquidacion_id = request.POST.get('liquidacion_id')
        liquidacion = Liquidacion.objects.get(id=liquidacion_id)
        liquidacion.pagar()
        messages.success(request, f"Se ha registrado el pago con exito.")
        return redirect(reverse('listarPagosProfesor'))




#--------------------------------CLASE---------------------------------------------


class ClaseDeleteView(DeleteView):
    model = Clase
    success_url = reverse_lazy('listarClases')
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ClaseDetailView(DetailView):
    model = Clase
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ClaseListView(ListView):
    model = Clase
    paginate_by = 100 
    

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

