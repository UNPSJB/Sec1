from dataclasses import fields
from sqlite3 import Row
from django import forms 
from apps.personas.models import Persona
from apps.personas.forms import PersonaForm
from django.forms import ValidationError, ModelForm, Textarea
from .models import Especialidad, Aula, Profesor, Curso, Dictado, Clase, Alumno, PagoDictado, Titularidad, Liquidacion, AsistenciaProfesor 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column
import ipdb

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = "__all__"

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

        labels = {
            'numero': 'Numero',
            'capacidad': 'Capacidad',
        }

    def clean(self):
        pass

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Aula</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                "Datos de Aula",
            Row(
                Column('numero', css_class='form-group col-md-4 mb-0'),
                Column('capacidad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),

            Submit('submit', 'Guardar', css_class='button white'),)

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = "__all__"
        exclude = ['tipo','persona']
        labels = {
            'aniosExperiencia': 'Años de experiencia',     
        }

class CrearProfesorForm(forms.Form):

    def clean_dni(self):
        self.persona = Persona.objects.filter(dni=self.cleaned_data['dni']).first()
        if self.persona is not None and self.persona.es_profesor:
            raise ValidationError("Ya existe un profesor con ese DNI")
        return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        personaForm = PersonaForm(self.data)
        profesorForm = ProfesorForm(self.data)
        valid = super().is_valid() and personaForm.is_valid() and profesorForm.is_valid()
        #self.cleaned_data.update(personaForm.cleaned_data)
        #self.cleaned_data.update(alumnoForm.cleaned_data)
        print(self.cleaned_data)
        return valid
    
    def save(self, commit=False):
        print(self.cleaned_data)
        if self.persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            self.persona = personaForm.save()
        profesorForm = ProfesorForm(data=self.cleaned_data)
        profesor = profesorForm.save(commit=False)
        self.persona.serProfesor(profesor)
        return profesor

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
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
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                Column('especializacion', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('aniosExperiencia', css_class='form-group col-md-4 mb-0'),
                Column('cbu', css_class='form-group col-md-4 mb-0'),
                Column('nacimiento', css_class='form-group col-md-4 mb-0'),
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = "__all__"

        widgets = {
            "desde": forms.TextInput(attrs={'type': 'date'}),
            "hasta": forms.TextInput(attrs={'type': 'date'}),
        }

        labels = {
            'desde': 'Fecha desde',
            'hasta': 'Fecha hasta',
            'formaPago': 'Forma de pago',
            'especialidad': 'Especialidad',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Curso</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Curso",
            Row(
                Column('especialidad', css_class='form-group col-md-4 mb-0'),
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('desde', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('hasta', css_class='form-group col-md-4 mb-0'),
                Column('cupo', css_class='form-group col-md-4 mb-0'),
                Column('cantModulos', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('formaPago', css_class='form-group col-md-4 mb-0'),
                Column('descuento', css_class='form-group col-md-4 mb-0'),
                Column('precio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class TitularidadForm(forms.ModelForm):
    class Meta:
        model = Titularidad
        fields = "__all__"
        #exclude = ['dictado']
        widgets = {
                "desde": forms.TextInput(attrs={'type': 'date'}),
                "hasta": forms.TextInput(attrs={'type': 'date'}),
        }

        labels = {
                'desde': 'Fecha Desde',
                'hasta': 'Fecha Hasta',
        }

class DictadoForm(forms.ModelForm):
    class Meta:
        model = Dictado
        fields = "__all__"
        exclude = ['profesor']
        widgets = {
                "inicio": forms.TextInput(attrs={'type': 'date'}),
                "fin": forms.TextInput(attrs={'type': 'date'}),
        }

        labels = {
                'inicio': 'Fecha inicio',
                'fin': 'Fecha fin',
        }

class CrearDictadoForm(forms.Form):
    


    def is_valid(self):
        #quiero crear el dictado para despues usarlo en la titularidad
        #pero no puedo avanzar porque la titularidad sin dictado no es valida
        #para ver que pasa le agregue que dictado puede ser null en titularidad
        dictadoForm = DictadoForm(self.data)
        titularidadForm = TitularidadForm(self.data)
        print('dictado form',dictadoForm.is_valid())
        print('titularidad form',titularidadForm.is_valid())
        valid = super().is_valid() and dictadoForm.is_valid() and titularidadForm.is_valid()
        # if not valid:
        #     self.errors.update(dictadoForm.errors)
        #     self.errors.update(titularidadForm.errors)
        return valid

    def save(self, commit=False):
        print('llego al save')
        dictadoForm = DictadoForm(data=self.cleaned_data)
        dictado = dictadoForm.save() 
        titularidadForm = TitularidadForm(data=self.cleaned_data)
        titularidad = titularidadForm.save() 
        profesor = self.cleaned_data['profesor']
        curso = self.cleaned_data['curso']
        desde = self.cleaned_data['desde']
        hasta = self.cleaned_data['hasta']
        costo = self.cleaned_data['costo']
        inicio = self.cleaned_data['inicio']
        fin = self.cleaned_data['fin']
        print(hasta)
        dictado.agregarDictado(curso, costo, inicio, fin)
        titularidad.agregarTitularidad(profesor, dictado, desde, hasta)
        print(profesor)
        #dictado.profesor.set(profesor)
        print(dictado)
        return dictado

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Dictado</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Dictado",
            Row(
                Column('aula', css_class='form-group col-md-4 mb-0'),
                Column('curso', css_class='form-group col-md-4 mb-0'),
                Column('costo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('inicio', css_class='form-group col-md-4 mb-0'),
                Column('fin', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),),     
            Fieldset(
                   "Datos Titularidad",
            Row(
                Column('profesor', css_class='form-group col-md-4 mb-0'),
                Column('desde', css_class='form-group col-md-4 mb-0'),
                Column('hasta', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)


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
                Column('dictado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

class PagoDictadoForm(forms.ModelForm):
    class Meta:
        model = PagoDictado
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
        exclude = ['persona','tipo', 'dictado']

        
class CrearAlumnoForm(forms.Form):
    curso = forms.ModelChoiceField(queryset= Curso.objects.all())
    
    def clean_dni(self):
        curso = self.cleaned_data['curso']
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni']) # para traer objetos específicos usamos .get() en lugar de .filter() que nos devolvería un queryset con 1 o más objetos.
            alumno = Alumno.objects.get(curso=curso, persona=persona)
        except Persona.DoesNotExist:
            persona = None
        except Alumno.DoesNotExist:
            alumno = None

        if persona is not None and alumno is not None:
            # en este caso sabemos que la persona existe en la bd y que además es alumno/a en el curso
            raise ValidationError("Ya existe un alumno con ese DNI")
        return self.cleaned_data['dni'] # todo marcha bien Milhouse (?, se devuelve el dni tal como ingresó.

    def is_valid(self):
        #personaForm = PersonaForm(self.data) # No es necesario. para validar el DNI en este caso usamos clean_dni() en este form. Podemos añadir mas clean_<campo> para validar los demás campos si fuera necesario
        alumnoForm = AlumnoForm(self.data)
        valid = super().is_valid() and alumnoForm.is_valid()
        if not valid:
            self.errors.update(alumnoForm.errors)
        return valid

    def save(self, commit=False):
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni'])
        except Persona.DoesNotExist:
            persona = None

        if persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            persona = personaForm.save()
        alumnoForm = AlumnoForm(data=self.cleaned_data)
        alumno = alumnoForm.save(commit=False)
        curso = self.cleaned_data['curso']
        persona.inscribir(alumno, self.cleaned_data['curso'])
        return alumno

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
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
                Column('nacimiento', css_class='form-group col-md-4 mb-0'),
                Column('curso', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),   

            Submit('submit', 'Guardar', css_class='button white'),)
        

CrearDictadoForm.base_fields.update(DictadoForm.base_fields)
CrearDictadoForm.base_fields.update(TitularidadForm.base_fields)


CrearProfesorForm.base_fields.update(PersonaForm.base_fields)
CrearProfesorForm.base_fields.update(ProfesorForm.base_fields)

CrearAlumnoForm.base_fields.update(AlumnoForm.base_fields)
CrearAlumnoForm.base_fields.update(PersonaForm.base_fields)

