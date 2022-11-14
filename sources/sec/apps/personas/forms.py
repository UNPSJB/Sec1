from .models import Persona, Vinculo
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet, ValidationError
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
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese nombre completo'}),
            "apellido": forms.TextInput(attrs={'placeholder': 'Ingrese apellido completo'}),
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

from django_select2 import forms as s2forms

class PersonaWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "dni__icontains",
        "nombre__icontains",
        "apellido__icontains",
    ]

class VinculoForm(forms.ModelForm):
    class Meta:
        model = Vinculo
        fields = ("tipoVinculo",
                  "vinculado")
        widgets = {
            'vinculado': PersonaWidget
        }

class BaseVinculoFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.template = 'bootstrap5/table_inline_formset.html'
        self.helper.add_input(Submit('submit', 'Guardar'))
    
    def clean(self):
        personas = [p['vinculado'].id for p in self.cleaned_data if 'vinculado' in p.keys()]
        if len(set(personas)) != len(personas):
            raise ValidationError("Solo puede existir un tipo de relacion con una persona")
        # Validar no tener vinculos recursivos

VinculoFormSet = modelformset_factory(Vinculo, form=VinculoForm, formset=BaseVinculoFormSet,
    extra=1,
    can_delete=True
)