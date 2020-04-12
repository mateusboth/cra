from django.test import SimpleTestCase
from datetime import date, timedelta
from calendario.forms import CalendarioForm
from django.core.exceptions import ValidationError

# Create your tests here.


class CalendarioFormTest(SimpleTestCase):
    def test_calendario_form_inicio_solicitacoes_field_label(self):
        form = CalendarioForm()
        self.assertEqual(
            form.fields['inicio_solicitacoes'].label, 'Inicío das Solicitações')

    def test_calendario_form_inicio_solicitacoes_field_help_text(self):
        form = CalendarioForm()
        self.assertEqual(form.fields['ano'].help_text,
                         'Ano dos pedidos, ex: 2020')

    def test_calendario_form_solicitacao_fim_before_inicio(self):
        ontem = date.today() - timedelta(days=1)
        form = CalendarioForm(
            data={'inicio_solicitacoes': date.today(), 'fim_solicitacoes': ontem})
        self.assertFalse(form.is_valid())

    def test_calendario_form_recursos_fim_before_inicio(self):
        ontem = date.today() - timedelta(days=1)
        form = CalendarioForm(
            data={'inicio_recursos': date.today(), 'fim_recursos': ontem, 'inicio_solicitacoes': ontem, 'fim_solicitacoes': date.today()})
        self.assertFalse(form.is_valid())
