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
        #Widgets ={
         #   'fechaNacimiento': forms.DateInput(attrs={'type':'datetime-local'}),
          #  }

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

