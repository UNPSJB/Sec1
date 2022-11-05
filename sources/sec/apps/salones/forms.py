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

class AlquilerForm(forms.ModelForm):
    
    class Meta:
        model = Alquiler
        fields = "__all__"
        exclude = ['salon']

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


    def is_valid(self) -> bool:
        valid = super().is_valid()
        salonForm = SalonForm(data=self.cleaned_data)
        return valid and salonForm.is_valid()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'cursos:index'
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
                #Column('encargado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)
        
#SalonForm.base_fields.update(PersonaForm.base_fields)
#SalonForm.base_fields.update(EmpresaForm.base_fields)     