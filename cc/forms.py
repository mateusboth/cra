"""SolicitacaoForm usado para criar solicitacoes de CC."""
from django_select2 import forms as s2forms
from crispy_forms.layout import HTML, Fieldset
from crispy_forms.helper import FormHelper, Layout
from django.forms import modelformset_factory
from datetime import date, timedelta
from django import forms
from .models import Solicitacao, Disciplina, Resultado, Recurso
from calendario.models import Calendario
from django.contrib.auth import get_user_model
User = get_user_model()


class SolicitacaoForm(forms.ModelForm):
    """Utiliza o usario e restringe as solicitacoes"""
    class Meta():
        model = Solicitacao
        fields = ['disciplina', 'justificativa', 'documentos']
        widgets = {  # TODO mudar DB para postersql e adiciona unaccent em search fields
            'disciplina': s2forms.ModelSelect2Widget(model=Disciplina,
                                                     search_fields=[
                                                         'nome__icontains', 'codigo__icontains'],
                                                     attrs={'data-minimum-input-length': 0,}),

        }

    def __init__(self, *args, **kwargs):
        """Definie user como o user passado em get_kwargs"""
        user = kwargs.pop('user')
        super(SolicitacaoForm, self).__init__(*args, **kwargs)
        self.instance.solicitante = user
        self.instance.semestre_solicitacao = Calendario.objects.filter(
            is_active=True).first()
        if not user.is_staff:  # filtra as disciplinas com base no curso do user
            self.fields['disciplina'].queryset = Disciplina.objects.filter(
                curso=user.curso)
        self.fields['disciplina'].help_text = "Disciplinas com acento deve ser maisuculas, ex: TÉCN"

    def clean(self, *args, **kwargs):
        """Impede pedidos repetidos, e mais de 3 pedidos em calendario vigente"""
        super().clean(*args, **kwargs)
        # Get the values
        disciplina = self.cleaned_data['disciplina']
        solicitante = self.instance.solicitante

        # Todos os pedidos no calendario
        user_pedidos = Solicitacao.objects.filter(solicitante=solicitante)
        user_pedidos_sem = user_pedidos.filter(
            semestre_solicitacao=self.instance.semestre_solicitacao).count()

        # Limita a três pedidos nos calendario
        if user_pedidos_sem >= 3:
            raise forms.ValidationError(
                'Somente três pedidos por semestre', code='quantidade')

        # Encontra pedidos repetidos e impede a solicitação
        duplicates = user_pedidos.filter(disciplina=disciplina)
        if self.instance.pk:
            # if the instance is already in the database,  exclude self from list of duplicates
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError(
                'Não é permitido solicitar duas vezes a mesma disciplina!', code='repetido')


def form_homologacao_valid(form):
    """Ajusta o reusltaod de homologada conforme valor de cursou_anteriormente e cria resultado"""
    if form.instance.cursou_anteriormente is True:
        form.instance.homologada = 'NAO'
    elif form.instance.cursou_anteriormente is False:
        form.instance.homologada = 'SIM'
    else:
        form.instance.homologada = 'PEN'
    # Verifica se ja existe um resultado associado
    r = Resultado.objects.filter(solicitacao=form.instance.pk)
    if form.instance.homologada != 'SIM':
        # deleta resultado se existir
        r.delete()
    if form.instance.homologada == 'SIM':
        s = Solicitacao.objects.get(pk=form.instance.pk)
        if not r:  # Se não existir um resultado cria um
            r = Resultado(solicitacao=s)
            r.save()


class AvaliadorForm(forms.ModelForm):
    """Defini avaliador"""
    class Meta():
        model = Resultado
        fields = ['avaliador']
        widgets = {  # TODO mudar DB para postersql e adiciona unaccent em search fields
            'avaliador': s2forms.ModelSelect2Widget(
                model=User,
                search_fields=[
                    'nome_completo__icontains',
                    'matricula__icontains'],
                attrs={'data-minimum-input-length': 0,
                'style': 'width: 100%;, min-width:80px'}),
        }

    def __init__(self, *args, **kwargs):
        """Definie user como o user passado em get_kwargs"""
        super(AvaliadorForm, self).__init__(*args, **kwargs)
        # filtra os avaliadores com base no is_avaliador
        self.fields['avaliador'].queryset = User.objects.filter(
            is_avaliador=True)
        # self.fields['avaliador'].help_text = "Nome com acento deve ser maisuculas, ex: JOÃO"


class ResultadoForm(forms.ModelForm):
    """Recebe a nota, e com base nela e na nota informa resultado"""
    class Meta():
        model = Resultado
        fields = ['solicitacao', 'nota']

    def __init__(self, *args, **kwargs):
        """Definie avaliador e solicitacao passado em get_kwargs"""
        avaliador = kwargs.pop('user', None)
        super(ResultadoForm, self).__init__(*args, **kwargs)
        if avaliador is not None and not avaliador.is_staff:
            self.instance.avaliador = avaliador
        self.fields['solicitacao'].disabled = True

class RecursoForm(forms.ModelForm):
    class Meta():
        model = Recurso
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Definie avaliador e solicitacao passado em get_kwargs"""
        solicitante = kwargs.pop('request')
        super(RecursoForm, self).__init__(*args, **kwargs)
        self.instance.solicitante = solicitante
