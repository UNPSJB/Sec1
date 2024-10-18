from dataclasses import fields
from sqlite3 import Row
from django import forms 

from apps.personas.models import Persona
from apps.personas.forms import PersonaForm, ModificarPersonaForm
from django.forms import ValidationError
from .models import Afiliado, Comercio, Familiar
from apps.personas.models import Persona 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column
from django.forms.models import model_to_dict
from datetime import date

class ComercioForm(forms.ModelForm):
    class Meta:
        model = Comercio
        fields = "__all__"

        widgets = {
            "cuit": forms.TextInput(attrs={'placeholder': 'Ingrese cuit','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "razonSocial": forms.TextInput(attrs={'placeholder': 'Ingrese razón social'}),
            "domicilio": forms.TextInput(attrs={'placeholder': 'Ingrese domicilio'}),
            "rama": forms.TextInput(attrs={'placeholder': 'Ingrese rama de la empresa'}),
        }
        labels = {
            'razonSocial': 'Razon social',
            'domicilio': 'Domicilio de la empresa',
        }
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control'
            if self.fields[field].required:
                self.fields[field].label = f'{self.fields[field].label}<span class="asteriskField">*</span>'
            # Si se está pasando una instancia, agregar el atributo disabled
            if instance:
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class FamiliarForm(forms.ModelForm):
    class Meta:
        model = Familiar
        fields = "__all__"
        exclude = ['persona','tipo','desde']

        widgets = {
            "afiliado": forms.HiddenInput,
            "relacion": forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'relacion': 'Tipo de relacion',
        }
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control'
            if self.fields[field].required:
                self.fields[field].label = f'{self.fields[field].label}<span class="asteriskField">*</span>'


class PersonaFamiliarForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['dni', 'nombre', 'apellido', 'nacimiento', 'nacionalidad']
        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese nombres','oninput': "this.value = this.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');""this.value = this.value.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');" }),
            "apellido": forms.TextInput(attrs={'placeholder': 'Ingrese apellidos', 'oninput': "this.value = this.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');" "this.value = this.value.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');"}),
            "nacimiento": forms.TextInput(attrs={'type': 'date'}),
            "nacionalidad": forms.TextInput(attrs={'placeholder': 'Ingrese nacionalidad'}),
        }
        labels = {
            'nacimiento': 'Fecha de nacimiento',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control'
            if self.fields[field].required:
                self.fields[field].label = f'{self.fields[field].label}<span class="asteriskField">*</span>'


class AfiliadoForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = "__all__"
        exclude = ['persona','tipo', 'familia','desde','hasta','alta']
        
        widgets = {
            "ingresoTrabajo": forms.TextInput(attrs={'type': 'date'}),
            "cuil": forms.TextInput(attrs={'placeholder': 'Ingrese cuil','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "jornadaLaboral": forms.TextInput(attrs={'placeholder': 'Ingrese jornada laboral','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "sueldo": forms.TextInput(attrs={'placeholder': 'Ingrese sueldo','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "comercio": forms.HiddenInput
        }
        labels = {
            'ingresoTrabajo': 'Fecha de ingreso al trabajo',
            'jornadaLaboral': 'Jornada laboral',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control'
            if self.fields[field].required:
                self.fields[field].label = f'{self.fields[field].label}<span class="asteriskField">*</span>'


class ModificarAfiliadoForm(forms.Form):
    def is_valid(self) -> bool:
        return super().is_valid() and self.personaForm.is_valid() and self.afiliadoForm.is_valid()
        
    def save(self):
        p = self.personaForm.save()
        return self.afiliadoForm.save()
        
    def __init__(self, initial=None, instance=None, *args, **kwargs):
        if instance is not None:
            self.personaForm = ModificarPersonaForm(initial=initial, instance=instance.persona, *args, **kwargs)
            self.afiliadoForm = AfiliadoForm(initial=initial, instance=instance, *args, **kwargs)
        else:
            self.personaForm = ModificarPersonaForm(initial=initial, *args, **kwargs)
            self.afiliadoForm = AfiliadoForm(initial=initial, *args, **kwargs)
        initial = dict(self.personaForm.initial)
        initial.update(self.afiliadoForm.initial)
        super().__init__(initial=initial, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Modificar Afiliado</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Personales",
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('apellido', css_class='form-group col-md-4 mb-0'),
                Column('nacimiento', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cuil', css_class='form-group col-md-4 mb-0'),
                Column('nacionalidad', css_class='form-group col-md-4 mb-0'),
                Column('estadoCivil', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('jornadaLaboral', css_class='form-group col-md-4 mb-0'),
                Column('sueldo', css_class='form-group col-md-4 mb-0'),
                Column('ingresoTrabajo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Column('comercio'),
            HTML('<hr/>'),
            Submit('submit', 'Guardar', css_class='button white'),)

ModificarAfiliadoForm.base_fields.update(ModificarPersonaForm.base_fields)
ModificarAfiliadoForm.base_fields.update(AfiliadoForm.base_fields)