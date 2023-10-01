from django import forms
from .models import Registro_Paciente, Registro_Historia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Field,Div,HTML

class RegistroPacienteForm(forms.ModelForm):
    email = forms.EmailField(label="Correo Electronico")
    nombre_madre = forms.CharField(label="Nombre de la Madre")
    cedula_madre = forms.CharField(label="Cedula de la Madre")
    class Meta:
        model = Registro_Paciente
        fields = (
            'nombre', 'apellido',  'fecha_nacimiento','edad','direccion','telefono','REF_Dr','nombre_madre','cedula_madre',
             'email',   'antecedentes_personales', 'pn', 'tn','antecedentes_familiares','enfermedad_actual'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<h1>Historia Médica</h1>'),
            Div(
                Div(Field('apellido', css_class='form-control'), css_class='col-6'),
                Div(Field('nombre', css_class='form-control'), css_class='col-6'),
                Div(Field('fecha_nacimiento', css_class='form-control'),css_class='col-6'),
                Div(Field('edad', css_class='form-control'), css_class='col-6'),
                Div(Field('direccion', css_class='form-control'), css_class='col-6'),
                Div(Field('telefono', css_class='form-control'), css_class='col-6'),
                Div(Field('REF_Dr', css_class='form-control'), css_class='col-8'),
                Div(Field('nombre_madre', css_class='form-control'), css_class='col-6'),
                Div(Field('cedula_madre', css_class='form-control'), css_class='col-6'),
                Div(Field('email', css_class='form-control'), css_class='col-8'),
                Div(Field('antecedentes_personales', css_class='form-control'), css_class='col-10'),
                Div(Field('pn', css_class='form-control'), css_class='col-1'),
                Div(Field('tn', css_class='form-control'), css_class='col-1'),
                Div(Field('antecedentes_familiares', css_class='form-control'), css_class='col-12'),
                Div(Field('enfermedad_actual', css_class='form-control'), css_class='col-12'),
                css_class='row'
            ),
            
            
        )
        self.helper.add_input(Submit('submit', 'Registrar' ,css_class=' mt-2'))

class RegistroHistoriaForm(forms.ModelForm):
    class Meta:
        model = Registro_Historia
        fields = ('peso','talla','ta','examen_fisico','laboratorio_ingreso','dx_ingreso','plan')
        
        
    def __init__(self, *args, **kwargs):
        super(RegistroHistoriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h1>Examen Fisico</h1>'),
            Div(
                Div(Field('peso', css_class='form-control'), css_class='col-4'),
                Div(Field('talla', css_class='form-control'), css_class='col-4'),
                Div(Field('ta', css_class='form-control'),css_class='col-4'),
                Div(Field('examen_fisico', css_class='form-control'), css_class='col-12'),
                Div(Field('laboratorio_ingreso', css_class='form-control'), css_class='col-12'),
                Div(Field('dx_ingreso', css_class='form-control'), css_class='col-12'),
                Div(Field('plan', css_class='form-control'), css_class='col-12'),
                css_class='row'
            ),
            Submit('submit', 'Registrar Historia',css_class='btn btn-primary mt-2 ')  # Agrega un botón de submit
        )