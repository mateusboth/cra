from django.forms import ModelForm, DateInput, ValidationError, CheckboxInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django.urls import reverse_lazy
from .models import Calendario


class CalendarioForm(ModelForm):
    """Formulário para criar um calendario. Configura layout do form"""
    class Meta():
        """Altera para o formato de data os inputs necessarios"""
        model = Calendario
        fields = ('is_active', 'ano', 'semestre', 'inicio_solicitacoes',
                  'fim_solicitacoes', 'inicio_recursos', 'fim_recursos')
        widgets = {
            'inicio_solicitacoes': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'fim_solicitacoes': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'inicio_recursos': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'fim_recursos': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        """Definir o layout utilizado pelo crispy form no template"""
        super(CalendarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            HTML('{% if form.instance.ano %} <h3>Editar calendário</h3> {% else %} <h3>Adicionar novo calendário</h3>{% endif %}'),
            'is_active',
            Row(
                Column('ano', css_class='form-group col-md-4 col-lg-2 mb-0'),
                Column('semestre', css_class='form-group col-md-4 col-lg-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('inicio_solicitacoes',
                       css_class='form-group col-md-4 col-lg-2 mb-0'),
                Column('fim_solicitacoes',
                       css_class='form-group col-md-4 col-lg-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('inicio_recursos',
                       css_class='form-group col-md-4 col-lg-2 mb-0'),
                Column('fim_recursos',
                       css_class='form-group col-md-4 col-lg-2 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Confirmar', css_class='btn btn-success')
        )

    def clean(self):
        """Garante que data de inicio é antes de data fim"""
        super(CalendarioForm, self).clean()
        if self.cleaned_data['inicio_solicitacoes'] > self.cleaned_data['fim_solicitacoes']:
            raise ValidationError(
                'Data de fim das solicitações deve ser posterior a de inicio')
        if self.cleaned_data['inicio_recursos'] > self.cleaned_data['fim_recursos']:
            raise ValidationError(
                'Data de fim das recursos deve ser posterior a de inicio')
