from dataclasses import fields
from sqlite3 import Row
from django import forms 
from apps.personas.models import Persona
from apps.personas.forms import PersonaForm, ModificarPersonaForm
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
            'aniosExperiencia': 'A??os de experiencia',     
        }

class CrearProfesorForm(forms.Form):

    def clean_dni(self):
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni'])
            profesor = Profesor.objects.get(persona=persona, hasta=None)
        except Persona.DoesNotExist:
            persona = None
        except Profesor.DoesNotExist:
            profesor = None

        if persona is not None and profesor is not None:
            raise ValidationError("Ya existe un profesor activo con ese DNI")
        return self.cleaned_data['dni']

    def is_valid(self) -> bool:
        #personaForm = PersonaForm(self.data)
        profesorForm = ProfesorForm(self.data)
        valid = super().is_valid() and profesorForm.is_valid()
        if not valid:
            self.errors.update(profesorForm.errors)
        print(self.cleaned_data)
        return valid
    
    def save(self, commit=False):
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni'])
        except Persona.DoesNotExist:
            persona = None

        if persona is None:
            personaForm = PersonaForm(data=self.cleaned_data)
            persona = personaForm.save()
        profesorForm = ProfesorForm(data=self.cleaned_data)
        profesor = profesorForm.save(commit=False)
        persona.serProfesor(profesor)
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

class ModificarProfesorForm(forms.Form):
    def is_valid(self) -> bool:
        return super().is_valid() and self.personaForm.is_valid() and self.profesorForm.is_valid()

    def save(self):
        p = self.personaForm.save()
        return self.profesorForm.save()

    def __init__(self, initial=None, instance=None, *args, **kwargs):
        if instance is not None:
            self.personaForm = ModificarPersonaForm(initial=initial, instance=instance.persona, *args, **kwargs)
            self.profesorForm = ProfesorForm(initial=initial, instance=instance, *args, **kwargs)
        else:
            self.personaForm = ModificarPersonaForm(initial=initial, *args, **kwargs)
            self.profesorForm = ProfesorForm(initial=initial, *args, **kwargs)
        initial = dict(self.personaForm.initial)
        initial.update(self.profesorForm.initial)
        super().__init__(initial=initial, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                '<h2><center>Modificar Profesor</center></h2>'),
            HTML(
                '<hr2/>'),
            Fieldset(
                    "Datos personales",
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('apellido', css_class='form-group col-md-4 mb-0'),
                Column('nacimiento', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('especializacion', css_class='form-group col-md-4 mb-0'),
                Column('aniosExperiencia', css_class='form-group col-md-4 mb-0'),
                Column('cbu', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
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
            'cupo': 'Cupo minimo',
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
                Column('modulos', css_class='form-group col-md-4 mb-0'),
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
        exclude=['dictado', 'hasta']
        widgets = {
                "desde": forms.TextInput(attrs={'type': 'date'}),
                #"hasta": forms.TextInput(attrs={'type': 'date'}),
        }

        labels = {
                'desde': 'Fecha Desde',
                #'hasta': 'Fecha Hasta',
        }

class DictadoForm(forms.ModelForm):
    class Meta:
        model = Dictado
        fields = "__all__"
        exclude = ['profesores', 'curso', 'costo'] # excluimos el campo ManyToMany
        widgets = {
                "inicio": forms.TextInput(attrs={'type': 'date'}),
                "fin": forms.TextInput(attrs={'type': 'date'}),
        }

        labels = {
                'inicio': 'Fecha inicio',
                'fin': 'Fecha fin',
        }

class CrearDictadoForm(forms.Form):

    def save(self, commit=False):
        dictadoForm = DictadoForm(self.cleaned_data)
        profesor = self.cleaned_data['profesor']
        desde = self.cleaned_data['desde']
        dictado = dictadoForm.save(commit=False)
        curso = self.initial["curso"]
        dictado.curso = curso
        dictado.costo = curso.precio
        dictado.save()
        dictado.agregarTitularidad(profesor, desde) # completamos los datos faltantes de titularidad (ver Model de Dictado).
        return dictado

    def __init__(self, initial=None, instance=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
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
        exclude = ['dictado']
        widgets = {
                'inicio' : forms.TimeInput(format='%H:%M',attrs={'type': 'time'}),
                'fin' : forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

        labels = {
                'inicio': 'Fecha inicio',
                'fin': 'Fecha fin',
        }
    def save(self, commit=False):
        clase = super().save(commit)
        clase.dictado = self.initial["dictado"]
        clase.save()
        return clase

    def __init__(self, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Clase</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Clase",
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
        exclude = ['dictado']
        widgets = {
                "pago": forms.TextInput(attrs={'type': 'date'}),
        }

        labels = {
                'pago': 'Fecha pago',
                'tipoPago': 'Forma de pago',
        }

    def save(self, commit=False):
        pago_dictado = super().save(commit)
        pago_dictado.dictado = self.initial["dictado"]
        pago_dictado.save()
        return pago_dictado

    def __init__(self, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Pago de Dictado</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Pago de Dictado",
            Row(
                Column('alumno', css_class='form-group col-md-4 mb-0'),
                Column('pago', css_class='form-group col-md-4 mb-0'),
                Column('monto', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('tipoPago', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            Submit('submit', 'Guardar', css_class='button white'),)

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

class EditarAlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = "__all__"
        exclude = ['persona','tipo', 'dictado', 'curso']
        
class CrearAlumnoForm(forms.Form):
    curso = forms.ModelChoiceField(queryset= Curso.objects.all())
    
    def clean_dni(self):
        curso = self.cleaned_data['curso']
        try:
            persona = Persona.objects.get(dni=self.cleaned_data['dni']) # para traer objetos espec??ficos usamos .get() en lugar de .filter() que nos devolver??a un queryset con 1 o m??s objetos.
            alumno = Alumno.objects.get(curso=curso, persona=persona)
        except Persona.DoesNotExist:
            persona = None
        except Alumno.DoesNotExist:
            alumno = None

        if persona is not None and alumno is not None:
            # en este caso sabemos que la persona existe en la bd y que adem??s es alumno/a en el curso
            raise ValidationError("Ya existe un alumno con ese DNI")
        return self.cleaned_data['dni'] # todo marcha bien Milhouse (?, se devuelve el dni tal como ingres??.

    def is_valid(self):
        #personaForm = PersonaForm(self.data) # No es necesario. para validar el DNI en este caso usamos clean_dni() en este form. Podemos a??adir mas clean_<campo> para validar los dem??s campos si fuera necesario
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
        alumno.inscribir(persona, curso)
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
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                Column('telefono', css_class='form-group col-md-4 mb-0'),
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

class ModificarAlumnoForm(forms.Form):
    def is_valid(self) -> bool:
        return super().is_valid() and self.personaForm.is_valid() and self.alumnoForm.is_valid()
        
    def save(self):
        p = self.personaForm.save()
        return self.alumnoForm.save()

    def __init__(self, initial=None, instance=None, *args, **kwargs):
        if instance is not None:
            self.personaForm = ModificarPersonaForm(initial=initial, instance=instance.persona, *args, **kwargs)
            self.alumnoForm = EditarAlumnoForm(initial=initial, instance=instance, *args, **kwargs)
        else:
            self.personaForm = ModificarPersonaForm(initial=initial, *args, **kwargs)
            self.alumnoForm = EditarAlumnoForm(initial=initial, *args, **kwargs)
        initial = dict(self.personaForm.initial)
        initial.update(self.alumnoForm.initial)
        super().__init__(initial=initial, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Modificar Alumno</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                   "Datos Personales",
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('apellido', css_class='form-group col-md-4 mb-0'),
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(

                Column('telefono', css_class='form-group col-md-4 mb-0'),
                Column('nacimiento', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),   

            Submit('submit', 'Guardar', css_class='button white'),)


ModificarAlumnoForm.base_fields.update(EditarAlumnoForm.base_fields)
ModificarAlumnoForm.base_fields.update(ModificarPersonaForm.base_fields)        

CrearDictadoForm.base_fields.update(DictadoForm.base_fields)
CrearDictadoForm.base_fields.update(TitularidadForm.base_fields)


CrearProfesorForm.base_fields.update(PersonaForm.base_fields)
CrearProfesorForm.base_fields.update(ProfesorForm.base_fields)

ModificarProfesorForm.base_fields.update(ModificarPersonaForm.base_fields)
ModificarProfesorForm.base_fields.update(ProfesorForm.base_fields) 

CrearAlumnoForm.base_fields.update(AlumnoForm.base_fields)
CrearAlumnoForm.base_fields.update(PersonaForm.base_fields)

