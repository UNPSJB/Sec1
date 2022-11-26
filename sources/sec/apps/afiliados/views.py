from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
def listadoAfiliados(request):
    return render(request, 'listadoAfiliados.html', {})

# ---------------------------- Afiliado View ------------------------------------ #

class AfiliadoCreateView(CreateView):

    model = Afiliado
    form_class = CrearAfiliadoForm

    def get_success_url(self):
        return reverse_lazy('detallarAfiliado', kwargs={'pk': self.object.pk})
"""
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
"""

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

#class AfiliadoDeleteView(DeleteView):
#    model = Afiliado
#    success_url = reverse_lazy('')

class AfiliadoDetailView(DetailView):
    model = Afiliado

class AfiliadoListView(ListView):
    model = Afiliado
    paginate_by = 100 

