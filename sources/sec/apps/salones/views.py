from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

def listadoSalones(request):
    return render(request, 'listadoSalones.html', {})


# ---------------------------- Salon View ------------------------------------ #

class SalonCreateView(CreateView):

    model = Salon
    form_class = SalonForm
    # template_name = 'salones/salon_form.html' # template del form
    success_url = reverse_lazy('listarSalones')

    

    def post(self, *args, **kwargs):
        self.object = None
        salon_form = self.get_form()
        

        if salon_form.is_valid():
            salon = salon_form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Salon registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarSalones')
            return redirect('listarSalones')
        messages.add_message(self.request, messages.ERROR, salon_form.errors)
        return self.form_invalid(form=salon_form)

class SalonUpdateView(UpdateView):
    model = Salon
    form_class = SalonForm
    success_url = reverse_lazy("modificarSalon")
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
def salon_eliminar(request, pk):
    a = Salon.objects.get(pk=pk)
    a.delete()
    return redirect('listarSalones') 

#class SalonDeleteView(DeleteView):
#    model = Salon
#    success_url = reverse_lazy('listarSalones')

class SalonDetailView(DetailView):
    model = Salon

class SalonListView(ListView):
    model = Salon
    paginate_by = 100 

# ---------------------------- Alquiler View ------------------------------------ #

class AlquilerCreateView(CreateView):

    model = Alquiler
    form_class = AlquilerForm
    # template_name = 'alquileres/alquiler_form.html' # template del form
    success_url = reverse_lazy('listarAlquileres')
"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar alquiler"
        context['ayuda'] = 'crear_alquiler.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        alquiler_form = self.get_form()
        

        if alquiler_form.is_valid():
            alquiler = alquiler_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Alquiler registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, alquiler_form.errors)
        return self.form_invalid(form=alquiler_form)
"""
class AlquilerUpdateView(UpdateView):
    model = Alquiler
    form_class = AlquilerForm
    success_url = reverse_lazy("listarAlquileres")

def alquiler_eliminar(request, pk):
    a = Alquiler.objects.get(pk=pk)
    a.delete()
    return redirect('listarAlquileres') 

#class AlquilerDeleteView(DeleteView):
#    model = Alquiler
#    success_url = reverse_lazy('listarAlquileres')

class AlquilerDetailView(DetailView):
    model = Alquiler

class AlquilerListView(ListView):
    model = Alquiler
    paginate_by = 100 

# ---------------------------- Servicio View ------------------------------------ #

class ServicioCreateView(CreateView):

    model = Servicio
    form_class = ServicioForm
    # template_name = 'servicios/servicio_form.html' # template del form
    success_url = reverse_lazy('listarServicios')
"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar servicio"
        context['ayuda'] = 'crear_servicio.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        servicio_form = self.get_form()
        

        if servicio_form.is_valid():
            servicio = servicio_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Servicio registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, servicio_form.errors)
        return self.form_invalid(form=servicio_form)
"""