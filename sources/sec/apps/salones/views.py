from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

def listadoSalones(request):
    return render(request, 'listadoSalones.html', {})


# ---------------------------- Salon View ------------------------------------ #

class SalonCreateView(CreateView):

    model = Salon
    form_class = SalonForm
    # template_name = 'salones/salon_form.html' # template del form
    success_url = reverse_lazy('crearSalon')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar salon"
        context['ayuda'] = 'crear_salon.html'
        return context


    def post(self, *args, **kwargs):
        self.object = None
        salon_form = self.get_form()
        

        if salon_form.is_valid():
            salon = salon_form.save()
            #messages.add_message(self.request, messages.SUCCESS, 'Salon registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('')
            return redirect('')
        #messages.add_message(self.request, messages.ERROR, salon_form.errors)
        return self.form_invalid(form=salon_form)

# ---------------------------- Alquiler View ------------------------------------ #

class AlquilerCreateView(CreateView):

    model = Alquiler
    form_class = AlquilerForm
    # template_name = 'alquileres/alquiler_form.html' # template del form
    success_url = reverse_lazy('crearAlquiler')

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

# ---------------------------- Servicio View ------------------------------------ #

class ServicioCreateView(CreateView):

    model = Servicio
    form_class = ServicioForm
    # template_name = 'servicios/servicio_form.html' # template del form
    success_url = reverse_lazy('crearServicio')

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