'''Views do app CC'''
from extra_views import ModelFormSetView
from django.forms import modelformset_factory
from .forms import form_homologacao_valid
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import SolicitacaoForm, ResultadoForm, RecursoForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Solicitacao, Resultado


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
    # TODO filtrar aqui lista de disciplinas com base no usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.filter(disciplina__nome__startswith='tererm')
        if self.request.user.has_perm('can_add_resultado'):
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
    success_url = reverse_lazy('cc:solicitacoes')

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

class ResultadoUpdate(UpdateView):
    model = Resultado
    template_name = 'create_form_generic.html'
    form_class = ResultadoForm

    def get_form_kwargs(self):
        """inclui user aos kwargs passado ao init do form"""
        kwargs = super(ResultadoUpdate, self).get_form_kwargs()
        kwargs.update({'request': self.request.user})
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

