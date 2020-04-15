'''Views do app CC'''
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
    #TODO filtrar aqui lista de disciplinas com base no usuario

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
    fields = ['solicitante','disciplina', 'cursou_anteriormente']
    permission_required = 'user.staff'
    template_name = 'create_form_generic.html'
    success_url = reverse_lazy('cc:solicitacoes')


    def form_valid(self, form):
        """Ajusta o reusltaod de homologada conforme valor de cursou_anteriormente e cria resultado"""
        if form.instance.cursou_anteriormente:
            form.instance.homologada = False
        elif form.instance.cursou_anteriormente is False:
            form.instance.homologada = True            
        else:
            form.instance.homologada = None
        redirect_url = super(HomologacaoCreate, self).form_valid(form)
        if form.instance.homologada:
            s = Solicitacao.objects.get(pk=form.instance.pk)
            r = Resultado(solicitacao=s)
            r.save()
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
