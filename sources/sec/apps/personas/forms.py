from .models import Persona
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet, ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from django import forms


class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['dni','nombre','apellido','nacimiento','nacionalidad','estadoCivil','domicilio','telefono','email']
        widgets = {
            "dni": forms.TextInput(attrs={'pattern': '(\d{7}|\d{8})', 'placeholder': '########', 'title': 'Debe ser un Dni Valido', 'oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese nombres','oninput': "this.value = this.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');""this.value = this.value.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');" }),
            "apellido": forms.TextInput(attrs={'placeholder': 'Ingrese apellidos', 'oninput': "this.value = this.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');" "this.value = this.value.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');"}),
            "nacimiento": forms.TextInput(attrs={'type': 'date'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            "estadoCivil": forms.Select(attrs={'class': 'form-select'}),
            "domicilio": forms.TextInput(attrs={'placeholder': 'Ingrese domicilio'}),
            "telefono": forms.TextInput(attrs={'placeholder': 'Ingrese teléfono','oninput': "this.value = this.value.replace(/[^0-9+]/g, '');"}),
            "email": forms.TextInput(attrs={'placeholder': 'Ingrese E-mail'}),
        }
        labels = {
            'nacimiento': 'Fecha de nacimiento',
            'estadoCivil': 'Estado civil',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control'
            if self.fields[field].required:
                self.fields[field].label = f'{self.fields[field].label}<span class="asteriskField">*</span>'

class ModificarPersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'nacimiento','nacionalidad', 'estadoCivil', 'domicilio','telefono', 'email']
        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese nombres','oninput': "this.value = this.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');""this.value = this.value.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');" }),
            "apellido": forms.TextInput(attrs={'placeholder': 'Ingrese apellidos', 'oninput': "this.value = this.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');" "this.value = this.value.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');"}),
            "nacimiento": forms.TextInput(attrs={'type': 'date'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            "estadoCivil": forms.Select(attrs={'class': 'form-select'}),
            "domicilio": forms.TextInput(attrs={'placeholder': 'Ingrese domicilio'}),
            "telefono": forms.TextInput(attrs={'placeholder': 'Ingrese teléfono','oninput': "this.value = this.value.replace(/[^0-9+]/g, '');"}),
            "email": forms.TextInput(attrs={'placeholder': 'Ingrese E-mail'}),
        }
        labels = {
            'nacimiento': 'Fecha de nacimiento',
            'estadoCivil': 'Estado civil',
        }


from django_select2 import forms as s2forms

class PersonaWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "dni__icontains",
        "nombre__icontains",
        "apellido__icontains",
    ]

