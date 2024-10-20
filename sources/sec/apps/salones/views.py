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
from django_select2.forms import ModelSelect2Widget
from datetime import datetime

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
    
def cambiar_estado_salon(request):
    if request.method == 'POST':
        salon_id = request.POST.get('id')

        # Buscar el salón por ID
        salon = Salon.objects.get(id=salon_id)
        
        # Cambiar el estado de disponibilidad
        salon.disponible = not salon.disponible
        salon.save()

        # Retornar el nuevo estado y el ID del salón en la respuesta
        return JsonResponse({
            'nuevo_estado': salon.disponible,
            'salon_id': salon.id,
            'nombre': salon.nombre, 
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)

#TODO: Ver que sucede al darle click y arreglar el problema
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Por defecto, solo enviamos los servicios disponibles
        mostrar_todos = self.request.GET.get('mostrar_todos', 'false') == 'true'
        if not mostrar_todos:
            context['servicios'] = self.object.servicio_set.filter(disponible=True)
        else:
            context['servicios'] = self.object.servicio_set.all()
        return context

    def get(self, request, *args, **kwargs):
        # Si es una solicitud AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object = self.get_object()
            mostrar_todos = request.GET.get('mostrar_todos', 'false') == 'true'
            servicios = self.object.servicio_set.all() if mostrar_todos else self.object.servicio_set.filter(disponible=True)
            
            data = [{
                'id': servicio.id,
                'nombre': servicio.nombre,
                'descripcion': servicio.descripcion,
                'precio': servicio.precio,
                'obligatorio': servicio.obligatorio,
                'disponible': servicio.disponible
            } for servicio in servicios]
            
            return JsonResponse({'servicios': data})
            
        return super().get(request, *args, **kwargs)

class SalonListView(ListView):
    model = Salon
    paginate_by = 100 
    context_object_name = 'salones'


# ---------------------------- Alquiler View ------------------------------------ #
# TODO: Mejorar el calendario para incluir la cola de espera
class AlquilerCreateView(CreateView):

    model = Alquiler
    form_class = AlquilerForm

    def get_initial(self):
        initial = super().get_initial()
        salon_pk = self.kwargs.get('salon_pk')
        salon = Salon.objects.get(pk=salon_pk)
        initial['salon'] = salon
        initial['monto'] = salon.monto
        initial['senia'] = (salon.monto * 10) / 100
        initial['reserva'] = timezone.now().date()
        return initial
    
    def form_valid(self, form):
        salon_pk = self.kwargs.get('salon_pk')
        salon = get_object_or_404(Salon, pk=salon_pk)
        alquiler = form.save(commit=False)

        inicio = form.cleaned_data['inicio']
        alquiler_existente = Alquiler.objects.filter(
            salon=salon,
            inicio=inicio,
            activo=True
        ).exists()

        alquiler.salon = salon
        alquiler.monto = salon.monto
        alquiler.senia = (salon.monto * 10) / 100 #ver si le cobro seña a los que estan el lista de espera
        alquiler.reserva = timezone.now().date()

        afiliado_id = self.request.POST.get('afiliado_id')
        if afiliado_id:
            afiliado = get_object_or_404(Afiliado, id=afiliado_id)
            alquiler.afiliado = afiliado

        if alquiler_existente:
            alquiler.activo = False
            alquiler.save()         
            messages.add_message(self.request, messages.SUCCESS, 'Añadido a la lista de espera')
            return self.redirect_to_waitlist(salon_pk, inicio)
        else:
            alquiler.activo = True
            alquiler.save()
            messages.add_message(self.request, messages.SUCCESS, 'Alquiler registrado con éxito')
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('comprobante_senia', kwargs={'pk': self.object.pk})

    def redirect_to_waitlist(self, salon_pk, inicio):
    
        return redirect(reverse('lista_espera', kwargs={
            'salon_pk': salon_pk, 
            'inicio': inicio
        }))

    def form_invalid(self, form):
        return super().form_invalid(form)

def obtener_dias_ocupados(request, salon_pk):
    alquileres = Alquiler.objects.filter(salon_id=salon_pk).values('inicio')
    fechas_ocupadas = [alquiler['inicio'].strftime('%Y-%m-%d') for alquiler in alquileres]

    return JsonResponse(fechas_ocupadas, safe=False)
    
    
def comprobante_senia(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk)
    
    context = {
        'alquiler': alquiler,
    }

    return render(request, 'salones/comprobante_senia.html', context)

def buscar_afiliado(request):
    dni = request.GET.get('dni')
    try:
        persona = Persona.objects.get(dni=dni)
        
        afiliado = Afiliado.objects.filter(persona=persona, hasta__isnull=True).first()

        if afiliado:  
            data = {
                'afiliado_id': afiliado.id,
                'nombre_afiliado': f"{persona.nombre} {persona.apellido}"
            }
        else:
            data = {
                'error': 'Afiliado no valido'
            }

    except (Persona.DoesNotExist, Afiliado.DoesNotExist):
        data = {'error': 'No se encontró un afiliado con ese DNI.'}

    return JsonResponse(data)


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
# TODO: Hacer bajas logicas
class ServicioCreateView(CreateView):

    model = Servicio
    form_class = ServicioForm
    success_url = reverse_lazy('listarServicios')

    def form_valid(self, form):
        salon_id = self.request.POST.get('salon')  
        salon = get_object_or_404(Salon, pk=salon_id)  

        servicio = form.save(commit=False)
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

def crear_cuotas(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    cuotas = int(request.POST.get('cuotas'))
    
    monto_total = alquiler.monto
    monto_por_cuota = monto_total / cuotas

    for numero_cuota in range(1, cuotas + 1):
        PagoAlquiler.objects.create(
            alquiler=alquiler,
            cuotas=cuotas,
            monto=monto_por_cuota,
            pago= None,
            numero=numero_cuota
        )

    return redirect('detallarAlquiler', pk=alquiler_id)

#Se paga una cuota
def registrar_pago(request, pago_id):
    pago = get_object_or_404(PagoAlquiler, id=pago_id)
    pago.pago = datetime.now()
    pago.save()
    messages.success(request, f'Pago de la cuota N°{pago.numero} ha sido realizado exitosamente.')
    return redirect('detallarAlquiler', pk=pago.alquiler.id)

class PagoAlquilerListView(ListView):
    model = PagoAlquiler
    template_name = 'salones/listar_cuotas.html'
    
    def get_queryset(self):
        alquiler_id = self.kwargs['alquiler_id']
        cuotas = PagoAlquiler.objects.filter(alquiler_id=alquiler_id)
        return cuotas

class ListaEsperaView(ListView):
    model = Alquiler
    template_name = 'salones/lista_espera.html'

    def get_queryset(self):
        salon_pk = self.kwargs.get('salon_pk')
        inicio = self.kwargs.get('inicio')

        lista_espera = Alquiler.objects.filter(
            salon_id=salon_pk,
            inicio=inicio,
            activo=False
        )
        return lista_espera

def cancelar_alquiler(alquiler_id):
    alquiler = get_object_or_404(Alquiler, pk=alquiler_id)
    alquiler.activo = False
    alquiler.save()

# TODO: Arreglar la creacion de cuotas, intentar poner un if empty llamar a crear cuotas

# TODO: Implementar cola de espera, cambiar al afiliado actual y elegir uno en espera