from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from sec.decorators import staff_required
from django.utils.decorators import method_decorator

# ---------------------------- Persona View ------------------------------------ #

class PersonaCreateView(CreateView):

    model = Persona
    form_class = PersonaForm
    # template_name = 'afiliados/afiliado_form.html' # template del form
    success_url = reverse_lazy('listarPersonas')


    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



    def post(self, *args, **kwargs):
        self.object = None
        persona_form = self.get_form()
        

        if persona_form.is_valid():
            afiliado = persona_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Afiliado registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, afiliado_form.errors)
        return self.form_invalid(form=persona_form)

class PersonaUpdateView(UpdateView):
    model = Persona
    form_class = PersonaForm
    success_url = reverse_lazy("listarPersonas")


    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Persona modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

@staff_required
def persona_eliminar(request, pk):
    a = Persona.objects.get(pk=pk)
    a.delete()
    return redirect('') 

#class PersonaDeleteView(DeleteView):
#    model = Persona
#    success_url = reverse_lazy('')

class PersonaDetailView(DetailView):
    model = Persona


    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class PersonaListView(ListView):
    model = Persona
    paginate_by = 100 

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)