'''Views do app CC'''
from extra_views import ModelFormSetView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from calendario.models import Calendario
from .models import Solicitacao, Resultado
from .forms import SolicitacaoForm, ResultadoForm, RecursoForm, AvaliadorForm, form_homologacao_valid


class SolicitacaoCreate(LoginRequiredMixin, CreateView):
    '''View e form para criação de um pedido de CC'''
    model = Solicitacao
    success_url = reverse_lazy('cc:solicitacoes')
    form_class = SolicitacaoForm
    template_name = 'create_form_generic.html'

    def get_form_kwargs(self):
        """inclui user aos kwargs passado ao init do form"""
        kwargs = super(SolicitacaoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class SolicitacoesGenericList(LoginRequiredMixin, generic.ListView):
    model = Solicitacao
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.has_perm('can_add_resultado'):
            if self.kwargs.get('slug'):  # Filtra pelo semestre/slug
                cal = get_object_or_404(
                    Calendario, slug=self.kwargs.get('slug'))
                qs = qs.filter(semestre_solicitacao=cal)
            return qs
        qs = qs.filter(solicitante=self.request.user)
        return qs


class SolicitacaoDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Solicitacao
    #permission_required = 'user.staff'

    def test_func(self):
        """verifica se o usurio é o solicitante ou staff, do contrar"""
        try:
            solicitacao = Solicitacao.objects.filter(
                pk=self.kwargs.get('pk'))[0]
        except IndexError:  # segue adiante para pagina 404 não encontrado
            return True
        return (self.request.user == solicitacao.solicitante) or self.request.user.has_perms('staff')


class HomologacaoCreate(PermissionRequiredMixin, UpdateView):
    """View para inserir se o aluno cursou anteriormente a disciplina e homologar a solicitação"""
    model = Solicitacao
    fields = ['solicitante', 'disciplina', 'cursou_anteriormente']
    permission_required = 'user.staff'
    template_name = 'create_form_generic.html'
    success_url = reverse_lazy('cc:solicitacoes') #TODO adiciona slug se houver

    def form_valid(self, form):
        form_homologacao_valid(form)
        redirect_url = super(HomologacaoCreate, self).form_valid(form)
        return redirect_url


class HomologacaoFormSetView(ModelFormSetView):
    model = Solicitacao
    fields = ['cursou_anteriormente']
    template_name = 'cc/manage_homologacoes.html'
    success_url = reverse_lazy('cc:solicitacoes')
    factory_kwargs = {'extra': 0}
    # form_class = HomologaçãoForm para adicionar crispy TODO

    def get_queryset(self):
        slug = self.kwargs['slug']
        return super(HomologacaoFormSetView, self).get_queryset().filter(semestre_solicitacao__slug=slug)

    def formset_valid(self, formset):
        """Ajusta o reusltaod de homologada conforme valor de cursou_anteriormente e cria resultado"""
        for form in formset:
            form_homologacao_valid(form)
        redirect_url = super(HomologacaoFormSetView,
                             self).formset_valid(formset)
        return redirect_url


class AusenteFormSetView(ModelFormSetView):
    "Defini alunos ausentes em bloco, com base no semestre"
    model = Resultado
    fields = ['ausente']
    template_name = 'cc/manage_ausentes.html'
    success_url = reverse_lazy('cc:solicitacoes')
    factory_kwargs = {'extra': 0}

    def get_queryset(self):
        slug = self.kwargs['slug']
        return super(AusenteFormSetView, self).get_queryset().filter(solicitacao__semestre_solicitacao__slug=slug)


class AvaliadorFormSetView(PermissionRequiredMixin, ModelFormSetView):
    "Defini avaliadores em bloco, com base no semestre"
    model = Resultado
    template_name = 'cc/manage_avaliadores.html'
    success_url = reverse_lazy('cc:solicitacoes')
    factory_kwargs = {'extra': 0}
    permission_required = 'user.can_add_avaliador'
    form_class = AvaliadorForm

    def get_queryset(self):
        slug = self.kwargs['slug']
        return super(AvaliadorFormSetView, self).get_queryset().filter(solicitacao__semestre_solicitacao__slug=slug)


class ResultadoFormSetView(PermissionRequiredMixin, ModelFormSetView):
    "Defini Resultados em bloco, com base no semestre"
    model = Resultado
    template_name = 'cc/manage_resultados.html'
    success_url = reverse_lazy('cc:solicitacoes')
    factory_kwargs = {'extra': 0}
    permission_required = 'user.can_add_resultado'
    form_class = ResultadoForm

    def get_queryset(self):
        slug = self.kwargs['slug']
        return super(ResultadoFormSetView, self).get_queryset().filter(solicitacao__semestre_solicitacao__slug=slug, resultado='PEN')

    def get_formset_kwargs(self):
        """inclui user aos kwargs passado ao init do form"""
        kwargs = super(ResultadoFormSetView, self).get_formset_kwargs()
        return kwargs

    def formset_valid(self, formset):
        for form in formset:
            if not self.request.user.is_staff:
                form.instance.avaliador = self.request.user
        return super(ResultadoFormSetView, self).formset_valid(formset)
    
    def get_success_url(self):
        return reverse_lazy('cc:solicitacoes', kwargs={'slug': self.kwargs['slug']})


class ResultadoUpdate(UpdateView):
    model = Resultado
    template_name = 'create_form_generic.html'
    form_class = ResultadoForm

    def get_form_kwargs(self):
        """inclui user aos kwargs passado ao init do form"""
        kwargs = super(ResultadoUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class RecursoCreate(CreateView):
    model = Solicitacao
    template_name = 'create_form_generic.html'
    form_class = RecursoForm

    def get_form_kwargs(self):
        """inclui user aos kwargs passado ao init do form"""
        kwargs = super(RecursoCreate, self).get_form_kwargs()
        kwargs.update({'request': self.request.user})
        return kwargs
