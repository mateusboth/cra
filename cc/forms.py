"""SolicitacaoForm usado para criar solicitacoes de CC."""
from datetime import date, timedelta
from django import forms
from .models import Solicitacao, Disciplina, Resultado, Recurso

from django_select2 import forms as s2forms


class SolicitacaoForm(forms.ModelForm):
    """Utiliza o usario e restringe as solicitacoes"""
    class Meta():
        model = Solicitacao
        fields = ['disciplina', 'justificativa', 'documentos']
        widgets = {
            'disciplina': s2forms.ModelSelect2Widget(model=Disciplina,
                            search_fields=['nome__icontains', 'codigo__icontains']),
        }

    def __init__(self, *args, **kwargs):
        """Definie user como o user passado em get_kwargs"""
        user = kwargs.pop('user')
        super(SolicitacaoForm, self).__init__(*args, **kwargs)
        self.instance.solicitante = user
        if not user.is_staff:  # filtra as disciplinas com base no curso do user
            self.fields['disciplina'].queryset = Disciplina.objects.filter(
                curso=user.curso)
        self.fields['disciplina'].help_text = "Digite CAX para exibir todas as disciplinas"

    def clean(self, *args, **kwargs):
        """Impede pedidos repetidos, e mais de 3 pedidos em 30 dias"""
        super().clean(*args, **kwargs)
        # Get the values
        disciplina = self.cleaned_data['disciplina']
        solicitante = self.instance.solicitante

        # Todos os pedidos
        user_pedidos = Solicitacao.objects.filter(solicitante=solicitante)

        # Limita a três pedidos nos últimos 30 dias
        n_pedidos_em_30_dias = user_pedidos.filter(
            data_solicitacao__gte=date.today() - timedelta(days=30)).count()
        if n_pedidos_em_30_dias >= 3:
            raise forms.ValidationError(
                'Somente três pedidos por semestre', code='quantidade')

        # Find the duplicates
        duplicates = user_pedidos.filter(disciplina=disciplina)
        if self.instance.pk:
            # if the instance is already in the database,  exclude self from list of duplicates
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError(
                'Não é permitido solicitar duas vezes a mesma disciplina!', code='repetido')


class ResultadoForm(forms.ModelForm):
    """Recebe a nota, e com base nela e na nota informa resultado"""
    class Meta():
        model = Resultado
        fields = ['solicitacao', 'nota', 'ausente']

    def __init__(self, *args, **kwargs):
        """Definie avaliador e solicitacao passado em get_kwargs"""
        avaliador = kwargs.pop('request')
        super(ResultadoForm, self).__init__(*args, **kwargs)
        self.instance.avaliador = avaliador
        self.fields['solicitacao'].disabled = True

    def clean(self, *args, **kwargs):  # TODO transferir para o save ?
        """Defini avaliador como usuario e o resultado conforme a nota"""
        super().clean(*args, **kwargs)
        if self.cleaned_data['ausente'] and self.cleaned_data['nota'] is not None:
            raise forms.ValidationError(
                'Aluno não pode estar ausente e ter nota')


class RecursoForm(forms.ModelForm):
    class Meta():
        model = Recurso
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Definie avaliador e solicitacao passado em get_kwargs"""
        solicitante = kwargs.pop('request')
        super(RecursoForm, self).__init__(*args, **kwargs)
        self.instance.solicitante = solicitante
