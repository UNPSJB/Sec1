from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# ---------------------------- Persona View ------------------------------------ #

class PersonaCreateView(CreateView):

    model = Persona
    form_class = PersonaForm
    # template_name = 'afiliados/afiliado_form.html' # template del form
    success_url = reverse_lazy('listarPersonas')


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

    
    def form_valid(self, form):
        #messages.add_message(self.request, messages.SUCCESS, 'Persona modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        #messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

def persona_eliminar(request, pk):
    a = Persona.objects.get(pk=pk)
    a.delete()
    return redirect('') 

#class PersonaDeleteView(DeleteView):
#    model = Persona
#    success_url = reverse_lazy('')

class PersonaDetailView(DetailView):
    model = Persona

class PersonaListView(ListView):
    model = Persona
    paginate_by = 100 

def FamiliaCreateView(request, pk):
    persona = Persona.objects.get(pk=pk)
    vinculos = list([{'tipoVinculo': v.tipoVinculo, 'vinculado': v.vinculado} for v in persona.vinculados.all()])
    if request.method == 'POST':
        formset = VinculoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for f in formset.forms:
                print(f)
    else:
        formset = VinculoFormSet(initial=vinculos)
    return render(request, 'personas/vinculo_form.html', {
        'formset': formset, 'persona': persona})