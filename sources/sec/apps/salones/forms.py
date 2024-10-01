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
from datetime import date
from django.utils import timezone


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
    class Meta:
        model = Alquiler
        fields = ['afiliado', 'inicio', 'senia']

        widgets = {
            "reserva": forms.TextInput(attrs={'type': 'date'}),
            "inicio": forms.TextInput(attrs={'type': 'date'}),
            "senia": forms.TextInput(attrs={'placeholder': 'Ingrese monto de la seña'}),
        }
        labels = {
            'senia': 'Seña',
            'reserva': 'Fecha de reserva',
            'inicio': 'Fecha de inicio'
        }

    def clean_senia(self):
        senia = self.cleaned_data['senia']
        if senia < 0 or senia > 99999999.99:
            raise forms.ValidationError("La senia no es valida")
        return senia

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


