from dataclasses import fields
from sqlite3 import Row
from django import forms 

from apps.personas.models import Persona
from apps.personas.forms import PersonaForm, ModificarPersonaForm
from django.forms import ValidationError
from .models import Afiliado, Empresa
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column
from django.forms.models import model_to_dict
from datetime import date

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
        exclude = ['persona','tipo', 'familia']
        
        widgets = {
            "ingresoTrabajo": forms.TextInput(attrs={'type': 'date'}),
            "cuil": forms.TextInput(attrs={'placeholder': 'Ingrese cuil'}),
            "nacionalidad": forms.TextInput(attrs={'placeholder': 'Ingrese nacionalidad'}),
            #"estadoCivil": forms.TextInput(attrs={'placeholder': 'Ingrese estado civil'}),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control'
            if self.fields[field].required:
                self.fields[field].label = f'{self.fields[field].label}<span class="asteriskField">*</span>'

class CrearAfiliadoForm(forms.Form):

    def clean_dni(self):
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni'])
            afiliado = Afiliado.objects.get(persona=persona, hasta=None)
        except Persona.DoesNotExist:
            persona = None
        except Afiliado.DoesNotExist:
            afiliado = None
        
        if persona is not None and afiliado is not None:
            raise ValidationError("Ya existe un afiliado activo con ese DNI")
        return self.cleaned_data['dni']
    
    def clean_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['nacimiento']
        if fecha_nacimiento:               
            if fecha_nacimiento >= date.today():
                raise forms.ValidationError("La fecha de nacimiento debe ser anterior a la fecha actual.")
        return self.cleaned_data['nacimiento']
    
    def clean_ingresoTrabajo(self):
        fecha_ingresoTrabajo = self.cleaned_data['ingresoTrabajo']
        if fecha_ingresoTrabajo:               
            if fecha_ingresoTrabajo > date.today():
                raise forms.ValidationError("La fecha de ingreso al trabajo tiene que ser valida")
        return self.cleaned_data['ingresoTrabajo']

    def is_valid(self) -> bool:
        #personaForm = PersonaForm(self.data)
        afiliadoForm = AfiliadoForm(self.data)
        valid = super().is_valid() and afiliadoForm.is_valid()
        if not valid:
            self.errors.update(afiliadoForm.errors)
        return valid 

    def save(self, commit=False):
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni'])
        except Persona.DoesNotExist:
            persona = None

        if persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            persona = personaForm.save()
        afiliadoForm = AfiliadoForm(data=self.cleaned_data)
        afiliado = afiliadoForm.save(commit=False)

        try:
            empresa = Empresa.objects.get(cuit=self.cleaned_data['cuit'])
        except Empresa.DoesNotExist:
            empresa = None

        if empresa is None:
            empresaForm = EmpresaForm(data=self.cleaned_data)
            empresa = empresaForm.save(commit=True)
        
        #TODO: clean empresa  para garantizzar la referancia 
        afiliado.empresa = empresa
        persona.afiliar(afiliado)
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
            Submit('submit', 'Guardar', css_class='button white'),)

ModificarAfiliadoForm.base_fields.update(ModificarPersonaForm.base_fields)
ModificarAfiliadoForm.base_fields.update(AfiliadoForm.base_fields)