from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
def listadoAfiliados(request):
    return render(request, 'listadoAfiliados.html', {})

# ---------------------------- Afiliado View ------------------------------------ #

class AfiliadoCreateView(CreateView):

    model = Afiliado
    form_class = AfiliadoForm
    # template_name = 'afiliados/afiliado_form.html' # template del form
    success_url = reverse_lazy('crearAfiliado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar afiliado"
        context['ayuda'] = 'crear_afiliado.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        afiliado_form = self.get_form()
        

        if afiliado_form.is_valid():
            afiliado = afiliado_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Afiliado registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, afiliado_form.errors)
        return self.form_invalid(form=afiliado_form)
