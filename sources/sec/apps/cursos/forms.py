from dataclasses import fields
from sqlite3 import Row
from django import forms 
from apps.personas.models import Persona
from apps.personas.forms import PersonaForm
from django.forms import ValidationError, ModelForm, Textarea
from .models import Especialidad, Aula, Profesor, Curso, Dictado, Clase, Alumno, PagoDictado, Titularidad, Liquidacion, AsistenciaProfesor 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = "__all__"

        labels = {
            'TIPOAREA': 'Area',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = nombre.lower()
        return nombre

    def clean(self):
        pass

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_action = 'especialidad:index'
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Especialidad</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                "Datos de Especialidad",
            Row(
                Column('area', css_class='form-group col-md-4 mb-0'),
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),

            Submit('submit', 'Guardar', css_class='button white'),)

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = "__all__"

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = "__all__"

    def clean_dni(self):
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_profesor:
            raise ValidationError("Ya existe un profesor con ese DNI")
        return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        valid = super().is_valid()
        personaForm = PersonaForm(data=self.cleaned_data)
        profesorForm = ProfesorForm(data=self.cleaned_data)
        return valid and personaForm.is_valid() and profesorForm.is_valid()

    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        profesorForm = ProfesorForm(data=self.cleaned_data)
        profesor = profesorForm.save(commit=False)
        self.persona.inscribirProfesor(profesor, self.cleaned_data['fecha_inscripcion'])
        return profesor
        #super().save(commit=commit)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'profesor:index'
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Profesor</center></h2>'),
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
                Column('direccion', css_class='form-group col-md-4 mb-0'),
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                Column('especializacion', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('añosExperiencia', css_class='form-group col-md-4 mb-0'),
                Column('cbu', css_class='form-group col-md-4 mb-0'),
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'curso:index'
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Curso</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Curso",
            Row(
                Column('TIPO', css_class='form-group col-md-4 mb-0'),
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('desde', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('hasta', css_class='form-group col-md-4 mb-0'),
                Column('cupo', css_class='form-group col-md-4 mb-0'),
                Column('modulos', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                #Column('profesor', css_class='form-group col-md-4 mb-0'),
                Column('descuento', css_class='form-group col-md-4 mb-0'),
                Column('precio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('formaPago', css_class='form-group col-md-4 mb-0'),
                #Column('especialidad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class DictadoForm(forms.ModelForm):
    class Meta:
        model = Dictado
        fields = "__all__"

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = "__all__"
    
    widgets = {
            "dia": forms.TextInput(attrs={'type': 'date'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'curso:index'
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Curso</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Curso",
            Row(
                Column('dia', css_class='form-group col-md-4 mb-0'),
                Column('inicio', css_class='form-group col-md-4 mb-0'),
                Column('fin', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                #Column('dictado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class PagoDictadoForm(forms.ModelForm):
    class Meta:
        model = PagoDictado
        fields = "__all__"

class TitularidadForm(forms.ModelForm):
    class Meta:
        model = Titularidad
        fields = "__all__"

class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = "__all__"

class AsistenciaProfesorForm(forms.ModelForm):
    class Meta:
        model = AsistenciaProfesor
        fields = "__all__"

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = "__all__"
        exclude = ['persona','tipo']

        widgets = {
            "fechaNacimiento": forms.TextInput(attrs={'type': 'date'}),
        }

        label = {
            "fechaNacimiento" : 'Fecha De Nacimiento'
        }
        
    def clean_dni(self):
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_alumno:
            raise ValidationError("Ya existe un alumno con ese DNI")
        return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        valid = super().is_valid()
        personaForm = PersonaForm(data=self.cleaned_data)
        alumnoForm = AlumnoForm(data=self.cleaned_data)
        return valid and personaForm.is_valid() and alumnoForm.is_valid()

    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        alumnoForm = AlumnoForm(data=self.cleaned_data)
        alumno = alumnoForm.save(commit=False)
        self.persona.inscribir(alumno, self.cleaned_data['fecha_inscripcion'])
        return alumno
        #super().save(commit=commit)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'alumnos:index'
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Alumno</center></h2>'),
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
                Column('fechaNacimiento', css_class='form-group col-md-4 mb-0'),
                Column('direccion', css_class='form-group col-md-4 mb-0'),
                Column('curso', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),   
            Fieldset(
                    "Datos Responsable",
            Row(
                Column('dni', css_class='form-group col-md-4 mb-0'),
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('apellido', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fechaNacimiento', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)
        
AlumnoForm.base_fields.update(PersonaForm.base_fields)