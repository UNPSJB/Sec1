from dataclasses import fields
from django import forms 

from apps.personas.models import Persona
from apps.personas.forms import PersonaForm
from django.forms import ValidationError
from .models import Afiliado, Empresa
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML



class AfiliadoForm(forms.ModelForm):
    
    class Meta:
        model = Afiliado
        fields = "__all__"
        exclude = ['tipo']

        #widgets = {
         #   "dni": forms.TextInput(attrs={'pattern': '(\d{7}|\d{8})', 'placeholder': '########'}),
        #}

    def clean_dni(self):
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_afiliado:
            raise ValidationError("Ya existe un afiliado activo con ese DNI")
        return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        valid = super().is_valid()
        personaForm = PersonaForm(data=self.cleaned_data)
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        return valid and personaForm.is_valid() and afiliadoForm.is_valid()

    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        afiliado = afiliadoForm.save(commit=False)
        self.persona.afiliar(afiliado, self.cleaned_data['fecha_afiliacion'])
        return afiliado
        #super().save(commit=commit)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'afiliados:index'
        self.helper.layout = Layout(
            HTML(
                    '<h2><center>Formulario de Afiliación</center></h2>'),
            Fieldset(
                   "Datos Personales",
                HTML(
                    '<hr/>'),
                    'dni', 
                    'nombre',
                    'apellido',
                    'fecha_nacimiento',
                    'direccion',
                    'mail',
                    'nacionalidad',
                    'estado_civil',
                    'cuil',
                    'celular',
            ),
            Submit('submit', 'Guardar', css_class='button white'),)
        
AfiliadoForm.base_fields.update(AfiliadoForm.base_fields)    