from django.shortcuts import render
from .forms import *
from .models import *
from apps.personas.forms import PersonaForm
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
def listadoAfiliados(request):
    return render(request, 'listadoAfiliados.html', {})


# ---------------------------- Afiliado de prueba View ------------------------------------ #

def crear_persona_y_afiliado(request):
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        afiliado_form = AfiliadoForm(request.POST)

        if persona_form.is_valid() and afiliado_form.is_valid():
            persona = persona_form.save()
            afiliado = afiliado_form.save(commit=False)
            afiliado.persona = persona

            # Validación de afiliaciones
            afiliados_existentes = Afiliado.objects.filter(persona=persona)

            for afiliado_existente in afiliados_existentes:
                if (afiliado_axistente.hasta is not None):
                    messages.error(request, "La persona ya tiene una afiliacion activa")
                    return render(request, 'afiliados/crear_persona_y_afiliado.html', {'persona_form': persona_form, 'afiliado_form': afiliado_form})

            afiliado.save()
            messages.success(request, "Persona y Afiliado creados exitosamente.")
            return redirect('/home')
        else:
            for field in persona_form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            for field in afiliado_form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo '{field.label}': {error}")
            return render(request, 'afiliados/crear_persona_y_afiliado.html', {'persona_form': persona_form, 'afiliado_form': afiliado_form})
    else:
        persona_form = PersonaForm()
        afiliado_form = AfiliadoForm()

    return render(request, 'afiliados/crear_persona_y_afiliado.html', {
        'persona_form': persona_form,
        'afiliado_form': afiliado_form,
    })

# ---------------------------- Afiliado View ------------------------------------ #

class AfiliadoCreateView(CreateView):

    model = Afiliado
    form_class = CrearAfiliadoForm

    def get_success_url(self):
        return reverse_lazy('detallarAfiliado', kwargs={'pk': self.object.pk})
    
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

