from dataclasses import fields
from sqlite3 import Row
from django import forms 
from apps.personas.models import Persona
from apps.personas.forms import PersonaForm, ModificarPersonaForm
from django.forms import ValidationError, ModelForm, Textarea
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML, Row, Column
import ipdb
from datetime import date


#--------------------------------ACTIVIDAD---------------------------------------------
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'descuento', 'categoria', 'tipoAbono', 'cupoReferencia', 'precioReferencia', 'remuneracionProfesor', 'diasTolerancia']
        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese Nombre de la activiad'}),
            "descripcion": forms.Textarea(attrs={'placeholder': 'Descripcion'}),
            "descuento": forms.TextInput(attrs={'placeholder': 'Descuento para afiliados','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "categoria": forms.Select(attrs={'class': 'form-select'}),
            "tipoAbono": forms.Select(attrs={'class': 'form-select'}),
            "cupoReferencia": forms.TextInput(attrs={'placeholder': 'Ingrese un Cupo de referencia','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "precioReferencia": forms.TextInput(attrs={'placeholder': 'Ingrese un Precio de referencia','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "remuneracionProfesor": forms.TextInput(attrs={'placeholder': 'Ingrese Remuneracion del Profesor','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "diasTolerancia": forms.TextInput(attrs={'placeholder': 'Ingrese los dias de tolerancia','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
        }

        labels = {
            'formaPago': 'Forma de pago',
            'especialidad': 'Especialidad',
            'cupoReferencia': 'Cupo de Referencia',
            'tipoAbono': 'Tipo de Abono',
            'precioReferencia': 'Precio de Referencia',
            'remuneracionProfesor': 'Remuneracion del Profesor',
            'diasTolerancia': 'Dias de Tolerancia'
        }
    """ 
    def clean_desde(self):
        fecha_desde = self.cleaned_data['desde']               
        if fecha_desde < date.today():
            raise forms.ValidationError("La fecha de inicio del curso no puede ser anterior a hoy")
        return fecha_desde

    def clean_hasta(self):
        fecha_hasta = self.cleaned_data['hasta']               
        if fecha_hasta < date.today():
            raise forms.ValidationError("La fecha de finalizacion del curso no puede ser anterior a hoy") 
        return fecha_hasta"""

    def clean_cupo(self):
        cupo = self.cleaned_data['cupoReferencia']
        if cupo < 5:
            raise forms.ValidationError("El cupo es insufuciente")
        if cupo > 999:
            raise forms.ValidationError("El cupo es demasiado grande")
        return cupo

    def clean_descuento(self):
        descuento = int(self.cleaned_data['descuento'])
        if descuento > 100:
            raise forms.ValidationError("El descuento es invalido")
        return descuento

    def clean_precio(self):
        precio = self.cleaned_data['precioReferencia']
        if precio > 999999:
            raise forms.ValidationError("El precio es invalido, el precio maximo es 999999")
        return precio

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if instance:
            self.helper.layout = Layout( 
                HTML(
                        '<h2><center>Editar Actividad</center></h2>'),
                HTML(
                        '<hr/>'),
                Fieldset(
                    "Datos de la Actividad",
                Row(
                    Column('nombre', css_class='form-group col-md-4 mb-0'),
                    Column('categoria', css_class='form-group col-md-4 mb-0'),
                    Column('tipoAbono', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('cupoReferencia', css_class='form-group col-md-4 mb-0'),
                    Column('precioReferencia', css_class='form-group col-md-4 mb-0'),
                    Column('remuneracionProfesor', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('descuento', css_class='form-group col-md-4 mb-0'),
                    Column('diasTolerancia', css_class='form-group col-md-4 mb-0'),
                    Column('descripcion', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                ),
                Submit('submit', 'Guardar', css_class='button white'),)
        else:
            self.helper.layout = Layout( 
                HTML(
                        '<h2><center>Registrar Actividad</center></h2>'),
                HTML(
                        '<hr/>'),
                Fieldset(
                    "Datos de la Actividad",
                Row(
                    Column('nombre', css_class='form-group col-md-4 mb-0'),
                    Column('categoria', css_class='form-group col-md-4 mb-0'),
                    Column('tipoAbono', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('cupoReferencia', css_class='form-group col-md-4 mb-0'),
                    Column('precioReferencia', css_class='form-group col-md-4 mb-0'),
                    Column('remuneracionProfesor', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('descuento', css_class='form-group col-md-4 mb-0'),
                    Column('diasTolerancia', css_class='form-group col-md-4 mb-0'),
                    Column('descripcion', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                ),
                Submit('submit', 'Guardar', css_class='button white'),)


#--------------------------------DICTADO---------------------------------------------
class DictadoForm(forms.ModelForm):
    dias = forms.MultipleChoiceField(
        choices=DIA,
        widget=forms.CheckboxSelectMultiple,
        label= 'Dias de Dictado'
    )
    class Meta:
        model = Dictado
        fields = ['aula','profesor','costo','cupo','inicio','fin','duracionClase','horaInicioClase','actividad']
        widgets = {
                "aula": forms.Select(attrs={'class': 'form-select'}),
                "profesor": forms.Select(attrs={'class': 'form-select'}),
                "costo": forms.NumberInput(attrs={'placeholder': 'Ingrese costo del curso'}),
                "cupo": forms.TextInput(attrs={'placeholder': 'Ingrese cupo del curso'}),
                "inicio": forms.TextInput(attrs={'type': 'date'}),
                "fin": forms.TextInput(attrs={'type': 'date'}),
                "duracioClase": forms.TextInput(),
                "horaInicioClase": forms.TextInput(attrs={'type': 'time'}),
                "actividad": forms.HiddenInput(),
        }

        labels = {
                'inicio': 'Fecha de inicio',
                'fin': 'Fecha de finalizacion',
                'duracionClase': 'Duracion de la clase',
                'horaInicioClase': 'Hora de Inicio'
        }

    def save(self, commit=True):
        dictado = super().save(commit=False)
        # Guarda los nombres de los días como una cadena separada por comas
        dias_nombres = [dict(DIA)[int(dia)] for dia in self.cleaned_data['dias']]  # Obtiene los nombres
        dictado.dias = ','.join(dias_nombres)  # Guarda como cadena
        if commit:
            dictado.save()
        dictado.generar_clases()
        dictado.generar_sueldo_profesor()
        return dictado

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'id': 'dictado-form'}
        if instance:
            self.helper.layout = Layout( 
                HTML(
                        '<h2><center>Editar Dictado</center></h2>'),
                HTML(
                        '<hr/>'),
                Fieldset(
                    "Datos del Dictado",
                Row(
                    Column('aula', css_class='form-group col-md-4 mb-0'),
                    Column('profesor', css_class='form-group col-md-4 mb-0'),
                    Column('cupo', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('costo', css_class='form-group col-md-4 mb-0'),
                    Column('inicio', css_class='form-group col-md-4 mb-0'),
                    Column('fin', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                ),
                Submit('submit', 'Guardar', css_class='button white'),)
        else:
            self.helper.layout = Layout( 
                HTML(
                        '<h2><center>Registrar Dictado</center></h2>'),
                HTML(
                        '<hr/>'),
                Fieldset(
                    "Datos del Dictado",
                Row(
                    Column('aula', css_class='form-group col-md-4 mb-0'),
                    Column('profesor', css_class='form-group col-md-4 mb-0'),
                    Column('cupo', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('costo', css_class='form-group col-md-4 mb-0'),
                    Column('inicio', css_class='form-group col-md-4 mb-0'),
                    Column('fin', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('duracionClase', css_class='form-group col-md-4 mb-0'),
                    Column('horaInicioClase', css_class='form-group col-md-4 mb-0'),
                    Column('dias', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row('actividad'),
                ),
                Submit('submit', 'Guardar', css_class='button white'),)


#--------------------------------AULA---------------------------------------------
class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = "__all__"

        labels = {
            'numero': 'Numero',
            'capacidad': 'Capacidad',
        }
    def clean_numero(self):
        numero = int(self.cleaned_data['numero'])
        if Aula.objects.filter(numero=numero).exists():
            raise forms.ValidationError("Ya existe un aula con este numero.")
        return numero
    
    def clean_capacidad(self):
        capacidad = int(self.cleaned_data['capacidad'])
        if capacidad <= 0 or capacidad > 999:
            raise forms.ValidationError("La capacidad no es valida")
        return capacidad

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'id': 'aula-form'}
        self.helper.layout = Layout( 
            HTML(
                    '<h2><center>Registrar Aula</center></h2>'),
            HTML(
                    '<hr/>'),
            Fieldset(
                "Datos de Aula",
            Row(
                Column('numero', css_class='form-group col-md-6 mb-0'),
                Column('capacidad', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),
            Submit('submit', 'Guardar', css_class='button white'),)


#--------------------------------PROFESOR---------------------------------------------
class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ["cbu", "experiencia"]
        widgets = {
            "cbu": forms.TextInput(attrs={'placeholder': 'Ingrese cbu','oninput': "this.value = this.value.replace(/[^0-9]/g, '');"}),
            "experiencia": forms.TextInput(attrs={'placeholder': 'Ingrese experiencia del profesor'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control'
            if self.fields[field].required:
                self.fields[field].label = f'{self.fields[field].label}<span class="asteriskField">*</span>'


#--------------------------------INSCRIPCION---------------------------------------------
class InscripcionDictadoForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ["alumno", "dictado"]
        widgets = {
            "alumno": forms.HiddenInput(),
            "dictado": forms.HiddenInput(),
        }

class InscripcionClaseForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ["alumno", "clase"]
        widgets = {
            "alumno": forms.HiddenInput(),
            "clase": forms.HiddenInput(),
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

    def clean_aniosExperiencia(self):
        aniosexp = self.cleaned_data['aniosExperiencia']
        if aniosexp < 0 or aniosexp > 99:
            raise forms.ValidationError("Los años de experiencia no son validos")
        return aniosexp

    def clean_cbu(self):
        cbu = self.cleaned_data['cbu']
        if Profesor.objects.filter(cbu=cbu).exists():
            raise forms.ValidationError("Ya existe un profesor con este cbu.")
        if cbu <= 0 or cbu > 9999999999999999999999:
            raise forms.ValidationError("El cbu no es valido")
        return cbu

    def clean_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['nacimiento']
        if fecha_nacimiento:               
            if fecha_nacimiento >= date.today():
                raise forms.ValidationError("La fecha de nacimiento debe ser anterior a la fecha actual.")
        return self.cleaned_data['nacimiento']

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
            HTML('<hr/>'),
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
                Column('nacionalidad', css_class='form-group col-md-4 mb-0'),
                Column('estadoCivil', css_class='form-group col-md-4 mb-0'),
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                Column('cbu', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('experiencia', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            HTML('<hr/>'),
            ),
        Submit('submit', 'Guardar', css_class='button white'),)





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
            HTML('<hr/>'),
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
        
""" class CrearAlumnoForm(forms.Form):
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

            Submit('submit', 'Guardar', css_class='button white'),) """

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
                Column('nacimiento', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nacionalidad', css_class='form-group col-md-4 mb-0'),
                Column('estadoCivil', css_class='form-group col-md-4 mb-0'),
                Column('domicilio', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ),
            HTML('<hr/>'),   
            Submit('submit', 'Guardar', css_class='button white'),)


ModificarAlumnoForm.base_fields.update(EditarAlumnoForm.base_fields)
ModificarAlumnoForm.base_fields.update(ModificarPersonaForm.base_fields)        

CrearProfesorForm.base_fields.update(PersonaForm.base_fields)
CrearProfesorForm.base_fields.update(ProfesorForm.base_fields)

ModificarProfesorForm.base_fields.update(ModificarPersonaForm.base_fields)
ModificarProfesorForm.base_fields.update(ProfesorForm.base_fields) 

