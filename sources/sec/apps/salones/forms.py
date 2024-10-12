from dataclasses import fields
from sqlite3 import Row
from django import forms 
import datetime

from apps.personas.models import Persona
from apps.personas.forms import PersonaForm
from apps.afiliados.models import Afiliado
from apps.afiliados.forms import AfiliadoForm
from django.forms import ValidationError
from .models import Salon, Servicio, Alquiler, PagoAlquiler
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column
from datetime import date
from django.utils import timezone

class EncargadoForm(forms.ModelForm):
    class Meta: 
        model = Persona
        fields = ['dni', 'nombre', 'apellido', 'telefono', 'domicilio', 'nacimiento']
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'domicilio': 'Domicilio',
            'nacimiento': 'Fecha de nacimiento',
        }

        hoy = datetime.date.today()
        fecha_limite = hoy - datetime.timedelta(days=18*365) 

        widgets = {
            'nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError("El DNI debe ser un número de 8 dígitos")
        return dni

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números")
        return telefono

    def clean_nacimiento(self):
        nacimiento = self.cleaned_data['nacimiento']
        hoy = datetime.date.today()
        fecha_limite = hoy - datetime.timedelta(days=18*365)

        if nacimiento > fecha_limite:
            raise forms.ValidationError("Debes ser mayor de 18 años para registrarte.")
        
        return nacimiento



    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h2><center>Registrar encargado</center></h2>'),
            HTML('<hr/>'),
            Fieldset(
                "Datos del encargado",
                Row(
                    Column('dni', css_class='form-group col-md-4 mb-0'),
                    Column('nombre', css_class='form-group col-md-4 mb-0'),
                    Column('apellido', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('telefono', css_class='form-group col-md-5 mb-0'),
                    Column('domicilio', css_class='form-group col-md-5 mb-0'),
                    Column('nacimiento', css_class='form-group col-md-5 mb-0'),
                    css_class='form-row'
                )
            ),
            Submit('submit', 'Guardar', css_class='button white'),
        )

class ServicioForm(forms.ModelForm):
    
    class Meta:
        model = Servicio
        fields = "__all__"
        #exclude = ['salon']

        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese nombre del servicio'}),
            "descripcion": forms.TextInput(attrs={'placeholder': 'Ingrese descripción'}),
        }

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Servicio</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos del Servicio",
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('descripcion', css_class='form-group col-md-4 mb-0'),
                Column('obligatorio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('salon', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),
            Submit('submit', 'Guardar', css_class='button white'),)

class AlquilerForm(forms.ModelForm):
    #salon = forms.ModelChoiceField(queryset= Salon.objects.all())
    #afiliado = forms.ModelChoiceField(queryset= Afiliado.objects.all())
    class Meta:
        model = Alquiler
        fields = "__all__"
        
        widgets = {
           "reserva": forms.TextInput(attrs={'type': 'date'}),
           "inicio": forms.TextInput(attrs={'type': 'date'}),
           "senia": forms.TextInput(attrs={'placeholder': 'Ingrese monto de la seña'}),
        }
        labels = {
            'senia': 'Seña',
            'reserva' : 'Fecha de reserva',
            'inicio' : 'Fecha  de inicio'
        }
"""
    def is_valid(self) -> bool:

        #afiliadoForm = AfiliadoForm(self.data)
        #salonForm = SalonForm(self.data)
        #alquilerForm = AlquilerForm(self.data)
        valid = super().is_valid() #and alquilerForm.is_valid()
        print(self.cleaned_data)
        #print(valid,afiliadoForm.is_valid(),salonForm.is_valid(),alquilerForm.is_valid())
        return valid

    def save(self, commit=False):
        print('llego aca')
        #afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        #afiliado = afiliadoForm.save(commit=False)
        #salonForm = SalonForm(data=self.cleaned_data)
        #salon = salonForm.save(commit=False)
        #alquilerForm = AlquilerForm(data=self.cleaned_data)
        alquiler = super.save(commit=False)
        alquiler.agregarAlquiler(self.cleaned_data['salon'], alquiler.senia, alquiler.reserva, alquiler.inicio, self.cleaned_data['afiliado']) #.agregarAlquiler(salon, alquiler.senia, alquiler.reserva, alquiler.inicio, afiliado)
        return alquiler

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Alquiler</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos del alquiler",
            Row(
                Column('afiliado', css_class='form-group col-md-4 mb-0'),
                Column('salon', css_class='form-group col-md-4 mb-0'),
                Column('senia', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('reserva', css_class='form-group col-md-4 mb-0'),
                Column('inicio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)
"""

class CrearAlquilerForm(forms.Form):
    salon = forms.ModelChoiceField(queryset= Salon.objects.all())
    afiliado = forms.ModelChoiceField(queryset= Afiliado.objects.all())
    def is_valid(self) -> bool:

        #afiliadoForm = AfiliadoForm(self.data)
        #salonForm = SalonForm(self.data)
        alquilerForm = AlquilerForm(self.data)
        valid = super().is_valid() and alquilerForm.is_valid()
        print(self.cleaned_data)
        #print(valid,afiliadoForm.is_valid(),salonForm.is_valid(),alquilerForm.is_valid())
        return valid
    
    def clean_senia(self):
        senia = self.cleaned_data['senia']
        if senia < 0 or senia > 99999999.99:
            raise forms.ValidationError("La senia no es valida")
        return senia

    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if monto < 0 or monto > 999999999.99:
            raise forms.ValidationError("El monto no es valido")
        return monto
    
    def clean_reserva(self):
        reserva = self.cleaned_data['reserva']               
        if reserva < date.today():
            raise forms.ValidationError("La fecha de reserva del lugar no puede ser anterior a hoy")
        return reserva
    
    def clean_inicio(self):
        inicio = self.cleaned_data.get('inicio')
        reserva = self.cleaned_data.get('reserva')
        if inicio and reserva and inicio < reserva:
            raise forms.ValidationError("La fecha de inicio del alquiler no puede ser anterior a la reserva")
        if reserva is None:
            return inicio
        return inicio
    
    def save(self, commit=False):
        print('llego aca')
        #afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        #afiliado = afiliadoForm.save(commit=False)
        #salonForm = SalonForm(data=self.cleaned_data)
        #salon = salonForm.save(commit=False)
        alquilerForm = AlquilerForm(data=self.cleaned_data)
        alquiler = alquilerForm.save(commit=False)
        alquiler.agregarAlquiler(self.cleaned_data['salon'], alquiler.senia, alquiler.reserva, alquiler.inicio, self.cleaned_data['afiliado']) #.agregarAlquiler(salon, alquiler.senia, alquiler.reserva, alquiler.inicio, afiliado)
        return alquiler

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Alquiler</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos del alquiler",
            Row(
                Column('afiliado', css_class='form-group col-md-4 mb-0'),
                Column('salon', css_class='form-group col-md-4 mb-0'),
                Column('senia', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('reserva', css_class='form-group col-md-4 mb-0'),
                Column('inicio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),
            Submit('submit', 'Guardar', css_class='button white'),)

class PagoAlquilerForm(forms.ModelForm):
    
    class Meta:
        model = PagoAlquiler
        fields = "__all__"
        #exclude = ['salon']

class SalonForm(forms.ModelForm):
    
    class Meta:
        model = Salon
        fields = "__all__"
        exclude = ['afiliado']
        
        labels = {
            'monto': 'Monto',   
        }

    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad < 0 or capacidad > 9999:
            raise forms.ValidationError("La capacidad no es valida")
        return capacidad

    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if monto < 0 or monto > 999999999.99:
            raise forms.ValidationError("El monto no es valido")
        return monto
    
    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Salon</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                "Datos del salon",
                       "Datos del salon",
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('direccion', css_class='form-group col-md-4 mb-0'),
                Column('capacidad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('monto', css_class='form-group col-md-4 mb-0'),
                Column('encargado', css_class='form-group col-md-4 mb-0'),
                Column('imagen',css_class = 'form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('descripcion', css_class = 'form-group col-md-10 mb-0'),
                css_class='form-row'


            )
            ),
            HTML('<hr/>'),
            Submit('submit', 'Guardar', css_class='button white'),)
        
CrearAlquilerForm.base_fields.update(PersonaForm.base_fields)
CrearAlquilerForm.base_fields.update(SalonForm.base_fields)
CrearAlquilerForm.base_fields.update(AlquilerForm.base_fields)
CrearAlquilerForm.base_fields.update(AfiliadoForm.base_fields)
     