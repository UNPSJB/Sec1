from django.shortcuts import render
from .forms import *
from .models import *
from apps.personas.forms import PersonaForm
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.forms.models import model_to_dict

# Create your views here.
def listadoAfiliados(request):
    return render(request, 'listadoAfiliados.html', {})


# ---------------------------- Afiliado de prueba View ------------------------------------ #
def buscar_persona_para_afiliado(request):
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
                afiliados_existentes = Afiliado.objects.filter(persona=persona)
                for afiliado_existente in afiliados_existentes:
                    if afiliado_existente.hasta is None:
                        afiliacion_activa = model_to_dict(afiliado_existente)
                        return JsonResponse({
                            'dni': dni,
                            'afiliacion_activa': afiliacion_activa,     
                        })
            except Persona.DoesNotExist:
                # Si no existe, crea un nuevo formulario vacío
                persona_form = PersonaForm()
                new_action = 'create'
            # Renderiza el formulario completo con los datos de la persona
            return render(request, 'afiliados/crear_afiliado_completo.html', {
                'persona_form': persona_form,
                'afiliado_form': AfiliadoForm(),
                'dni': dni,  # Manten el DNI para uso posterior
                'action': new_action
            })


def crear_persona_y_afiliado(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        # Manejo del formulario completo para guardar
        if action == 'update':
            dni = request.POST.get('dni')
            old_persona = Persona.objects.get(dni=dni)
            persona_form = PersonaForm(request.POST, instance=old_persona)
        else:
            persona_form = PersonaForm(request.POST)

        afiliado_form = AfiliadoForm(request.POST)

        if persona_form.is_valid() and afiliado_form.is_valid():
            persona = persona_form.save()
            afiliado = afiliado_form.save(commit=False)
            afiliado.persona = persona

            # Validación de afiliaciones
            afiliados_existentes = Afiliado.objects.filter(persona=persona)

            for afiliado_existente in afiliados_existentes:
                if afiliado_existente.hasta is None:
                    messages.error(request, "La persona ya tiene una afiliación activa")
                    return render(request, 'afiliados/crear_persona_y_afiliado.html', {
                        'persona_form': persona_form,
                        'afiliado_form': afiliado_form
                    })

            afiliado.save()
            messages.success(request, "Solicitud cargada exitosamente.")
            return redirect(reverse('detallarSolicitud', args=[afiliado.id]))
        else:
            # Manejar errores de validación
            for field in persona_form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            for field in afiliado_form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            return render(request, 'afiliados/crear_persona_y_afiliado.html', {
                'persona_form': persona_form,
                'afiliado_form': afiliado_form
            })

    # Si es un GET inicial, mostrar solo el formulario de DNI
    persona_form = PersonaForm()
    afiliado_form = AfiliadoForm()
    return render(request, 'afiliados/crear_persona_y_afiliado.html', {
        'persona_form': persona_form,
        'afiliado_form': afiliado_form
    })

def aceptar_solicitud(request, afiliado_id):
    if request.method == 'POST':
        afiliado = Afiliado.objects.get(id=afiliado_id)
        afiliado.darAlta()
        messages.success(request, f"Se acepto la solicitud de {afiliado}.")
        return redirect(reverse('afiliacionesPendientes'))

def desafiliar(request):
    if request.method == 'POST':
        afiliado_id = request.POST.get('afiliado_id')
        afiliado = Afiliado.objects.get(id=afiliado_id)
        motivo = request.POST.get('motivo')
        afiliado.desafiliar(motivo)
        messages.success(request, f"Se ha desafiliado a {afiliado}.")
        return redirect(reverse('listarAfiliados'))

def quitarFamiliar(request):
    if request.method == 'POST':
        familiar_id = request.POST.get('familiar_id')
        familiar = Familiar.objects.get(id=familiar_id)
        familiar.dejarDeSer()
        messages.success(request, f"Se ha quitado a {familiar}.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('crearAfiliado')))

def rechazar_solicitud(request):
    if request.method == 'POST':
        afiliado_id = request.POST.get('afiliado_id')
        afiliado = Afiliado.objects.get(id=afiliado_id)
        motivo = request.POST.get('motivo')
        afiliado.rechazar(motivo)
        messages.success(request, f"Se ha rechazado la solicitud de {afiliado}.")
        return redirect(reverse('afiliacionesPendientes'))

def buscar_comercio(request):
    if request.method == 'GET':
        comercio_cuit = request.GET.get('cuit')
        try:
            # Intenta obtener el comercio por el cuit
            comercio = Comercio.objects.get(cuit=comercio_cuit)
            comercio_form = ComercioForm(instance=comercio)
            action = 'detail'
            is_disabled = True
            comercio_id = comercio.id
        except Comercio.DoesNotExist:
            # Si no existe, crea un nuevo formulario vacío
            comercio_form = ComercioForm()
            action = 'create'
            is_disabled = False
            comercio_id = '' 
        # Renderiza el formulario completo con los datos del comercio
        return render(request, 'comercios/comercio.html', {
                'comercio_form': comercio_form,
                'cuit': comercio_cuit,  # Manten el cuit para uso posterior
                'action': action,
                'is_disabled': is_disabled,  # Pasa la variable is_disabled
                'id': comercio_id
        })

def crear_comercio(request):
    if request.method == 'POST':
        action = request.POST.get('action-comercio')
        if action == 'update':
            comercio_cuit = request.POST.get('cuit')
            old_comercio = Comercio.objects.get(cuit=comercio_cuit)
            comercio_form = ComercioForm(request.POST,instance=old_comercio)
        else:
            comercio_form = ComercioForm(request.POST)
        if comercio_form.is_valid():
            comercio = comercio_form.save()  # Guarda el comercio
            # Devuelve los datos de cuit y razonSocial
            return JsonResponse({
                'cuit': comercio.cuit,
                'razonSocial': comercio.razonSocial,
                'id': comercio.id
            })
        else:
            print('no se que mierda pasa')
    return JsonResponse({'error': 'Formulario no válido'}, status=400)

def buscar_persona_para_familiar(request):
    if request.method == 'GET':
        # Primero, verificar si se envió el formulario de DNI
        dni = request.GET.get('dni')
        try:
            # Intenta obtener la persona por el DNI
            persona = Persona.objects.get(dni=dni)
            if persona.es_afiliado:
                return JsonResponse({
                        'denegado': True,
                        'mensaje': 'La persona cuanta con una afiliacion activa'  
                        })
            if persona.es_familiar:
                return JsonResponse({
                        'denegado': True,
                        'mensaje': 'La persona ya esta vinculada a un afiliado'  
                        })
            persona_form = PersonaFamiliarForm(instance=persona)
            new_action = 'update'
            """afiliados_existentes = Afiliado.objects.filter(persona=persona)
            for afiliado_existente in afiliados_existentes:
                if afiliado_existente.hasta is None:
                    afiliacion_activa = model_to_dict(afiliado_existente)
                    return JsonResponse({
                        'dni': dni,
                        'afiliacion_activa': afiliacion_activa,     
                    }) """
        except Persona.DoesNotExist:
            # Si no existe, crea un nuevo formulario vacío
            persona_form = PersonaFamiliarForm()
            new_action = 'create'
        # Renderiza el formulario completo con los datos de la persona
        return render(request, 'familia/familiar.html', {
            'persona_form': persona_form,
            'familiar_form': FamiliarForm(),
            'dni': dni,  # Manten el DNI para uso posterior
            'action': new_action
        })

def crear_familiar(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        # Manejo del formulario completo para guardar
        if action == 'update':
            dni = request.POST.get('dni')
            old_persona = Persona.objects.get(dni=dni)
            persona_form = PersonaFamiliarForm(request.POST, instance=old_persona)
        else:
            persona_form = PersonaFamiliarForm(request.POST)

        familiar_form = FamiliarForm(request.POST)

        if persona_form.is_valid() and familiar_form.is_valid():
            persona = persona_form.save(commit=False)
            persona.es_familiar= True
            persona.save()
            familiar = familiar_form.save(commit=False)
            familiar.persona = persona
            familiar.save()
            messages.success(request, "Familiar cargado exitosamente.")
            return JsonResponse({
                'familiar': familiar.id,
            })
        else:
            # Manejar errores de validación
            
            for field in persona_form:
                for error in field.errors:
                    print(f"Error en el campo '{field.label}': {error}")
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            for field in familiar_form:
                for error in field.errors:
                    print(f"Error en el campo '{field.label}': {error}")
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            # return render(request, 'afiliados/crear_persona_y_afiliado.html', {
            #     'persona_form': persona_form,
            #     'afiliado_form': afiliado_form
            # })

# ---------------------------- Afiliado View ------------------------------------ #

""" class AfiliadoCreateView(CreateView):

    model = Afiliado
    form_class = CrearAfiliadoForm

    def get_success_url(self):
        return reverse_lazy('detallarAfiliado', kwargs={'pk': self.object.pk}) """
    
class AfiliadoUpdateView(UpdateView):
    model = Afiliado
    form_class = ModificarAfiliadoForm
    #success_url = reverse_lazy("detallarAfiliado")

    def get_success_url(self):
        return reverse_lazy('detallarAfiliado', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Afiliado"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Afiliado modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


def afiliado_eliminar(request, pk):
    a = Afiliado.objects.get(pk=pk)
    a.delete()
    return redirect('listarAfiliados') 

class AfiliadoDeleteView(DeleteView):
    model = Afiliado
    success_url = reverse_lazy('')

class AfiliadoDetailView(DetailView):
    model = Afiliado

class AfiliadoListView(ListView):
    model = Afiliado
    paginate_by = 100
    ordering = 'id'

class AfiliacionesPendientes(ListView):
    model = Afiliado
    paginate_by = 100
    template_name = 'afiliados/afiliaciones_pendientes.html'
    def get_queryset(self):
        # Filtra los afiliados que están pendientes
        return Afiliado.objects.filter(alta__isnull=True,hasta__isnull=True).order_by('id')

class AfiliacionPendienteDetailView(DetailView):
    model = Afiliado
    template_name = 'afiliados/afiliacion_pendiente_detail.html'
