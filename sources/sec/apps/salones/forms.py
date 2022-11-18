from dataclasses import fields
from sqlite3 import Row
from django import forms 

from apps.personas.models import Persona
from apps.personas.forms import PersonaForm
from apps.afiliados.models import Afiliado
from apps.afiliados.forms import AfiliadoForm
from django.forms import ValidationError
from .models import Salon, Servicio, Alquiler, PagoAlquiler
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column

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
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('direccion', css_class='form-group col-md-4 mb-0'),
                Column('capacidad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('monto', css_class='form-group col-md-4 mb-0'),
                Column('encargado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)
        
#CrearAlquilerForm.base_fields.update(PersonaForm.base_fields)
#CrearAlquilerForm.base_fields.update(SalonForm.base_fields)
CrearAlquilerForm.base_fields.update(AlquilerForm.base_fields)
#CrearAlquilerForm.base_fields.update(AfiliadoForm.base_fields)
     