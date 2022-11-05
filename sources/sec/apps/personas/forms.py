from .models import Persona
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from django import forms

class PersonaForm(ModelForm):
   
    class Meta:
        model = Persona
        fields = '__all__'
        exclude=['persona', 'tipo']
        widgets = {
            "dni": forms.TextInput(attrs={'pattern': '(\d{7}|\d{8})', 'placeholder': '########'}),
            "fechaNacimiento": forms.TextInput(attrs={'type': 'date'})
        }
        labels = {
            'fechaNacimiento': 'Fecha de nacimiento',
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'guardarAfiliado'
        self.helper.layout = Layout(
            Fieldset(
                   "",
                HTML(
                    '<hr/>'),
                    'dni', 
                    'nombre',
                    'apellido',
                    'fechaNacimiento',    
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

