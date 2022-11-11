from dataclasses import fields
from sqlite3 import Row
from django import forms 

from apps.personas.models import Persona
from apps.personas.forms import PersonaForm
from django.forms import ValidationError
from .models import Salon, Servicio, Alquiler, PagoAlquiler
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column

class ServicioForm(forms.ModelForm):
    
    class Meta:
        model = Servicio
        fields = "__all__"
        exclude = ['salon']

        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese nombre del servicio'}),
            "descripcion": forms.TextInput(attrs={'placeholder': 'Ingrese descripción'}),
        }

    def is_valid(self) -> bool:
        valid = super().is_valid()
        servicioForm = ServicioForm(data=self.cleaned_data)
        return valid and servicioForm.is_valid()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'servicio:index'
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
                #Column('salon', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)

class AlquilerForm(forms.ModelForm):
    
    class Meta:
        model = Alquiler
        fields = "__all__"
        #exclude = ['salon']
        widgets = {
           "reserva": forms.TextInput(attrs={'type': 'date'}),
           "inicio": forms.TextInput(attrs={'type': 'date'}),
           "seña": forms.TextInput(attrs={'placeholder': 'Ingrese monto de la seña'}),
        }
        labels = {
            'seña': 'Seña',
            'reserva' : 'Fecha de reserva',
            'inicio' : 'Fecha  de inicio'
        }

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        pass    

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
                #Column('afiliado', css_class='form-group col-md-4 mb-0'),
                #Column('salon', css_class='form-group col-md-4 mb-0'),
                Column('seña', css_class='form-group col-md-4 mb-0'),
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
        #exclude = ['persona','tipo']
        
        #widgets = {
         #   "fechaIngresoTrabajo": forms.TextInput(attrs={'type': 'date'})
        #}
        labels = {
            'montoSalon': 'Monto',
        }

    def clean(self):
        pass 

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
                Column('montoSalon', css_class='form-group col-md-4 mb-0'),
                Column('encargado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)
        
#SalonForm.base_fields.update(PersonaForm.base_fields)
     