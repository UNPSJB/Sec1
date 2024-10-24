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

import re

class EncargadoForm(forms.ModelForm):
    class Meta: 
        model = Persona
        fields = [ 'nombre', 'apellido', 'telefono','email', 'domicilio', 'nacionalidad', 'estadoCivil', 'nacimiento']
        labels = {
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
            'nombre': forms.TextInput(attrs={
                'pattern': '[a-zA-ZñÑáéíóúÁÉÍÓÚ ]*',
                'onkeypress': 'return /[a-zA-ZñÑáéíóúÁÉÍÓÚ ]/.test(event.key)',
                'oninput': 'this.value = this.value.split(" ").map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(" ");',
            }),
            'apellido': forms.TextInput(attrs={
                'pattern': '[a-zA-ZñÑáéíóúÁÉÍÓÚ ]*',
                'onkeypress': 'return /[a-zA-ZñÑáéíóúÁÉÍÓÚ ]/.test(event.key)',
                'oninput': 'this.value = this.value.split(" ").map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(" ");',
            }),
            'dni': forms.TextInput(attrs={
                'pattern': '[0-9]{8}',
                'maxlength': '8',
                'onkeypress': 'return /[0-9]/.test(event.key)',
            }),
            'domicilio': forms.TextInput(attrs={
                'pattern': '[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]*\\d+$',
                'oninput': 'this.value = this.value.replace(/[^a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]/g, "").split(" ").map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(" ");'
            }),
            "telefono": forms.TextInput(attrs={
                'oninput': "this.value = this.value.replace(/[^0-9+]/g, '');"
            }),
        }

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
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not re.match("^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$", nombre):
            raise forms.ValidationError("Nombre incorrecto.")
        return nombre.capitalize()

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not re.match("^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$", apellido):
            raise forms.ValidationError("Apellido incorrecto.")
        return apellido.capitalize()

    def clean_domicilio(self):
        domicilio = self.cleaned_data['domicilio']
        if not re.match("^[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]+$", domicilio):
            raise forms.ValidationError("El domicilio no debe contener símbolos.")
        if not re.search(r'\d+$', domicilio):
            raise forms.ValidationError("El domicilio debe contener un número al final.")
        return domicilio

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def __init__(self, *args, **kwargs):
        form_title = kwargs.pop('form_title', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(f'<h2><center>{form_title or "Registrar Encargado"}</center></h2>'),
            HTML('<hr/>'),
            Fieldset(
                "Datos del encargado",
                Row(
                    Column('nombre', css_class='form-group col-md-6 mb-3'),
                    Column('apellido', css_class='form-group col-md-6 mb-3'),
                    Column('telefono', css_class='form-group col-md-6 mb-3'),
                    Column('email', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('domicilio', css_class='form-group col-md-6 mb-3'),
                    Column('nacionalidad', css_class='form-group col-md-6 mb-3'),
                    Column('estadoCivil', css_class='form-group col-md-6 mb-3'),
                    Column('nacimiento', css_class='form-group col-md-6 mb-3'),
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
        fields = ['nombre', 'direccion', 'capacidad', 'monto', 'encargado', 'imagen', 'imagen2', 'imagen3', 'descripcion']
        exclude = ['afiliado']

        labels = {
            'monto': 'Monto (en pesos)',
            'imagen1': 'Imagen principal', 
            'imagen2': 'Imagen 2 (opcional)',
            'imagen3': 'Imagen 3 (opcional)',
        }

        widgets = {
            'capacidad': forms.NumberInput(attrs={
                'min': 0,
                'max': 999,
                'maxlength': 3,
                'oninput': '''
                    if (this.value.length > 3) {
                        this.value = this.value.slice(0, 3);  // Corta el valor a 3 dígitos
                    }
                    this.value = this.value.replace(/[^0-9]/g, "");  // Permite solo números
            ''',
                'placeholder': 'Ingrese capacidad'  
            }),
            'monto': forms.NumberInput(attrs={
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "");',
                'placeholder': 'Ingrese monto'  
            }),
            'nombre': forms.TextInput(attrs={
                'pattern': '[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]*',
                'oninput': 'this.value = this.value.replace(/[^a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]/g, "").split(" ").map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(" ");',
                'placeholder': 'Ingrese nombre del salón' 
            }),
            'direccion': forms.TextInput(attrs={
                'pattern': '[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]*\\d+$',
                'oninput': 'this.value = this.value.replace(/[^a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]/g, "").split(" ").map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(" ");',
                'placeholder': 'Ingrese dirección'  # Placeholder agregado
            }),
            'descripcion': forms.Textarea(attrs={
                'oninput': 'this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);',
                'placeholder': 'Ingrese descripción'  # Placeholder agregado
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'placeholder': 'Seleccionar imagen principal'  # Placeholder agregado
            }),
            'imagen2': forms.ClearableFileInput(attrs={
                'placeholder': 'Seleccionar imagen 2 (opcional)'  # Placeholder agregado
            }),
            'imagen3': forms.ClearableFileInput(attrs={
                'placeholder': 'Seleccionar imagen 3 (opcional)'  # Placeholder agregado
            }),
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
        form_title = kwargs.pop('form_title', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                f'<h2><center>{form_title or "Registrar Salon"}</center></h2>'),
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
                    Column('imagen2',css_class = 'form-group col-md-4 mb-0'),
                    Column('imagen3',css_class = 'form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('descripcion', css_class = 'form-group col-md-11 mb-0'),
                    css_class='form-row'


            )
            ),
        HTML('<hr/>'),
            Submit('submit', 'Guardar', css_class='button white'),
        )


   