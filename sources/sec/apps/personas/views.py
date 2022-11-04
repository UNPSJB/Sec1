from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# ---------------------------- Persona View ------------------------------------ #

class PersonaCreateView(CreateView):

    model = Persona
    form_class = PersonaForm
    # template_name = 'afiliados/afiliado_form.html' # template del form
    success_url = reverse_lazy('crearPersona')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar persona"
        context['ayuda'] = 'crear_persona.html'
        return context


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
