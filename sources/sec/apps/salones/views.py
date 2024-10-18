from django.shortcuts import render
import os
from django.conf import settings
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse

#TODO: Ver como hacer los editar para salones, encargados y servicios

def listadoSalones(request):
    return render(request, 'listadoSalones.html', {})



# ---------------------------- Encargado View ------------------------------------ #
class EncargadoCreateView(CreateView):
    model = Persona
    form_class = EncargadoForm
    success_url = reverse_lazy('listarEncargados')  

    def form_valid(self, form):
        encargado = form.save(commit=False)
        encargado.es_encargado = True  
        encargado.save()  
        return super().form_valid(form)


def eliminar_encargado(request, pk):
    encargado = get_object_or_404(Persona, pk=pk)
    encargado.es_encargado = False
    encargado.save()
    return JsonResponse({'status': 'success'})
class EncargadoListView(ListView):
    model = Persona
    paginate_by = 100 
    template_name = '../salones/templates/salones/encargado_list.html'

    def get_queryset(self):
        return Persona.objects.filter(es_encargado=1).order_by('dni')

# ---------------------------- Salon View ------------------------------------ #

class SalonCreateView(CreateView):

    model = Salon
    form_class = SalonForm

    def get_success_url(self):
        return reverse_lazy('detallarSalon', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        salon = form.save(commit=False)  
        salon.save() 
        messages.add_message(self.request, messages.SUCCESS, 'Salon registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    

def cambiar_estado(request):
    if request.method == 'POST':
        salon_id = request.POST.get('id')

        # Buscar el servicio por ID
        salon = Salon.objects.get(id=salon_id)
        
        # Cambiar el estado de disponibilidad
        salon.disponible = not salon.disponible
        salon.save()

        # Retornar el nuevo estado en la respuesta
        return JsonResponse({'nuevo_estado': salon.disponible})

    return JsonResponse({'error': 'Método no permitido'}, status=405)
class SalonUpdateView(UpdateView):
    model = Salon
    form_class = SalonForm
    success_url = reverse_lazy("modificarSalon")

def salon_eliminar(request, pk):
    a = Salon.objects.get(pk=pk)
    a.delete()
    return redirect('listarSalones') 

class SalonDeleteView(DeleteView):
    model = Salon
    success_url = reverse_lazy('listarSalones')




class SalonDetailView(DetailView):
    model = Salon
    context_object_name = 'salon'

class SalonListView(ListView):
    model = Salon
    paginate_by = 100 
    context_object_name = 'salones'


# ---------------------------- Alquiler View ------------------------------------ #

class AlquilerCreateView(CreateView):

    model = Alquiler
    form_class = AlquilerForm

    def get_initial(self):
        initial = super().get_initial()
        salon_pk = self.kwargs.get('salon_pk')
        salon = Salon.objects.get(pk=salon_pk)
        initial['salon'] = salon
        initial['monto'] = salon.monto
        initial['reserva'] = timezone.now().date()
        return initial
    

    def form_valid(self, form):
        salon_pk = self.kwargs.get('salon_pk')
        salon = get_object_or_404(Salon, pk=salon_pk)

        alquiler = form.save(commit=False)

        alquiler.salon = salon
        alquiler.monto = salon.monto
        alquiler.reserva = timezone.now().date()

        alquiler.save()

        messages.add_message(self.request, messages.SUCCESS, 'Alquiler registrado con éxito')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('comprobante_senia', kwargs={'pk': self.object.pk})
    
    def form_invalid(self, form):
        print(self.request.POST)
        return super().form_invalid(form)
    
def comprobante_senia(request, pk):
        alquiler = get_object_or_404(Alquiler, pk=pk)
        
        context = {
            'alquiler': alquiler,
            # Puedes agregar otros datos que desees mostrar en el comprobante
        }
        
        #return render(request, 'comprobante_senia.html', context)
        return render(request, 'salones/comprobante_senia.html', context)
class AlquilerUpdateView(UpdateView):
    model = Alquiler
    form_class = AlquilerForm
    success_url = reverse_lazy("listarAlquileres")

def alquiler_eliminar(request, pk):
    a = Alquiler.objects.get(pk=pk)
    a.delete()
    return redirect('listarAlquileres') 

class AlquilerDeleteView(DeleteView):
    model = Alquiler
    success_url = reverse_lazy('listarAlquileres')

class AlquilerDetailView(DetailView):
    model = Alquiler

class AlquilerListView(ListView):
    model = Alquiler
    paginate_by = 100 

# ---------------------------- Servicio View ------------------------------------ #

class ServicioCreateView(CreateView):

    model = Servicio
    form_class = ServicioForm
    success_url = reverse_lazy('listarServicios')

    def form_valid(self, form):
        salon_id = self.request.POST.get('salon')  
        salon = get_object_or_404(Salon, pk=salon_id)  

        servicio = form.save(commit=False)
        print(servicio.disponible)
        servicio.salon = salon  
        servicio.save()  
        messages.add_message(self.request, messages.SUCCESS, 'El servicio ha sido agregado con éxito.')

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detallarSalon', kwargs={'pk': self.object.salon.pk})

class ServicioUpdateView(UpdateView):
    model = Servicio
    form_class = ServicioForm
    success_url = reverse_lazy("listarServicios")

def servicio_eliminar(request, pk):
    a = Servicio.objects.get(pk=pk)
    a.delete()
    return redirect('listarServicios') 


def cambiar_estado(request):
    if request.method == 'POST':
        servicio_id = request.POST.get('id')

        # Buscar el servicio por ID
        servicio = Servicio.objects.get(id=servicio_id)
        
        # Cambiar el estado de disponibilidad
        servicio.disponible = not servicio.disponible
        servicio.save()

        # Retornar el nuevo estado en la respuesta
        return JsonResponse({'nuevo_estado': servicio.disponible})

    return JsonResponse({'error': 'Método no permitido'}, status=405)


class ServicioDeleteView(DeleteView):
    model = Servicio
    success_url = reverse_lazy('listarServicios')

class ServicioDetailView(DetailView):
    model = Servicio

class ServicioListView(ListView):
    model = Servicio
    paginate_by = 100 

def elegir_forma_pago(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk)
    
    if request.method == 'POST':
        forma_pago = request.POST.get('forma_pago')
        if forma_pago == 'unico':
            return redirect('pago_unico', pk=alquiler.pk)
        elif forma_pago == 'cuotas':
            return redirect('pago_cuotas', pk=alquiler.pk)

    return render(request, 'salones/elegir_forma_pago.html', {'alquiler': alquiler})

def pago_unico (request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk)

    if request.method == 'POST':
        monto = request.POST.get('monto')
        fecha_pago = timezone.now().date()
        #fecha_pago = request.POST.get('pago')

        PagoUnico.objects.create(
            alquiler=alquiler,
            monto=alquiler.monto,
            pago=fecha_pago
        )

        messages.success(request, "Pago realizado con exito")
        return redirect('detallarAlquiler', pk=alquiler.pk)
    return render(request, 'salones/pago_unico.html', {'alquiler': alquiler})
