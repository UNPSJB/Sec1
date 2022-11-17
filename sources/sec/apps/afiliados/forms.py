from dataclasses import fields
from sqlite3 import Row
from django import forms 

from apps.personas.models import Persona
from apps.personas.forms import PersonaForm
from django.forms import ValidationError
from .models import Afiliado, Empresa
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"

        widgets = {
            "cuit": forms.TextInput(attrs={'placeholder': 'Ingrese cuit'}),
            "razonSocial": forms.TextInput(attrs={'placeholder': 'Ingrese razón social'}),
            "domicilio": forms.TextInput(attrs={'placeholder': 'Ingrese domicilio'}),
            "rama": forms.TextInput(attrs={'placeholder': 'Ingrese rama de la empresa'}),
        }
        labels = {
            'razonSocial': 'Razon social',
            'domicilio': 'Domicilio de la empresa',
        }

class AfiliadoForm(forms.ModelForm):
    
    class Meta:
        model = Afiliado
        fields = "__all__"
        exclude = ['persona','tipo', 'familia', 'empresa']
        
        widgets = {
            "ingresoTrabajo": forms.TextInput(attrs={'type': 'date'}),
            "cuil": forms.TextInput(attrs={'placeholder': 'Ingrese cuil'}),
            "nacionalidad": forms.TextInput(attrs={'placeholder': 'Ingrese nacionalidad'}),
            "estadoCivil": forms.TextInput(attrs={'placeholder': 'Ingrese estado civil'}),
            "domicilio": forms.TextInput(attrs={'placeholder': 'Ingrese domicilio'}),
            "telefono": forms.TextInput(attrs={'placeholder': 'Ingrese teléfono'}),
            "email": forms.TextInput(attrs={'placeholder': 'Ingrese E-mail'}),
            "jornadaLaboral": forms.TextInput(attrs={'placeholder': 'Ingrese jornada laboral'}),
            "sueldo": forms.TextInput(attrs={'placeholder': 'Ingrese sueldo'}),
        }
        labels = {
            'domicilio': 'Domicilio',
            'ingresoTrabajo': 'Fecha de ingreso al trabajo',
            'estadoCivil': 'Estado civil',
            'jornadaLaboral': 'Jornada laboral',
        }

class CrearAfiliadoForm(forms.Form):

    def clean_dni(self):
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_afiliado:
            raise ValidationError("Ya existe un afiliado activo con ese DNI")
        return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        personaForm = PersonaForm(self.data)
        afiliadoForm = AfiliadoForm(self.data)
        valid = super().is_valid() and personaForm.is_valid() and afiliadoForm.is_valid()
        return valid 

    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        #afiliado = super().save(commit=False)
        afiliado = afiliadoForm.save(commit=False)
        empresaForm = EmpresaForm(data=self.cleaned_data)
        #TODO: clean empresa  para garantizzar la referancia 
        afiliado.empresa = empresaForm.save(commit=True)
        self.persona.afiliar(afiliado, self.cleaned_data.get('fecha_afiliacion'))
        return afiliado
        
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Afiliado</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Personales",
            Row(
                Column('dni', css_class='form-group col-md-4 mb-0'),
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('apellido', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nacimiento', css_class='form-group col-md-4 mb-0'),
                Column('cuil', css_class='form-group col-md-4 mb-0'),
                Column('nacionalidad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('estadoCivil', css_class='form-group col-md-4 mb-0'),
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-4 mb-0'),
                Column('jornadaLaboral', css_class='form-group col-md-4 mb-0'),
                Column('sueldo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ingresoTrabajo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),   
            Fieldset(
                    "Datos de Empresa",
            Row(
                Column('cuit', css_class='form-group col-md-4 mb-0'),
                Column('razonSocial', css_class='form-group col-md-4 mb-0'),
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('rama', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

CrearAfiliadoForm.base_fields.update(PersonaForm.base_fields)
CrearAfiliadoForm.base_fields.update(AfiliadoForm.base_fields)
CrearAfiliadoForm.base_fields.update(EmpresaForm.base_fields)     