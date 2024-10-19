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
        fields = ['nombre', 'descripcion', 'precio', 'obligatorio']
        exclude = ['salon']

        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese nombre del servicio'}),
            "descripcion": forms.TextInput(attrs={'placeholder': 'Ingrese descripción'}),
             "precio": forms.TextInput(attrs={'placeholder': 'Ingrese precio'}),

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
                    Column('precio', css_class='form-group col-md-4 mb-0'),

                    Column('obligatorio', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
            ),
            
            Submit('submit', 'Guardar', css_class='button white'),)


class AlquilerForm(forms.ModelForm):
    """ afiliado = forms.ModelChoiceField(queryset= Afiliado.objects.filter(desde__isnull = True),
                                      widget=forms.Select(attrs={'class': 'select2'})) """
   
    dni = forms.CharField(max_length=8, label='DNI', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el DNI'}))
    afiliado_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Alquiler
        fields = ['inicio']

        widgets = {
            "inicio": forms.TextInput(attrs={'type': 'date'})
        }
        labels = {
            'inicio': 'Fecha de inicio'
        }

    def clean_inicio(self):
        inicio = self.cleaned_data.get('inicio')
        reserva = timezone.now().date()
        if inicio and reserva and inicio < reserva:
            raise forms.ValidationError(
                "La fecha de inicio del alquiler no puede ser anterior a la reserva")
        if reserva is None:
            return inicio
        return inicio

class PagoAlquilerForm(forms.ModelForm):
    
    class Meta:
        model = PagoAlquiler
        fields = "__all__"
        #exclude = ['salon']

class SalonForm(forms.ModelForm):

    encargado = forms.ModelChoiceField(
        queryset=Persona.objects.filter(es_encargado=True),  
        required=True, 
        label='Encargado'
    )
    
    class Meta:
        model = Salon
        fields = ['nombre', 'direccion', 'capacidad', 'monto', 'encargado', 'imagen', 'descripcion']
        exclude = ['afiliado']

        labels = {
            'monto': 'Monto (en pesos)',
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
            Submit('submit', 'Guardar', css_class='button white'),
        )


   