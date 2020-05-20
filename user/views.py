from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm

User = get_user_model()

# Create your views here.

class UserCreateView(CreateView):
    """cadastre-se view"""
    template_name = 'create_form_generic.html'
    form_class = SignUpForm
    success_url = reverse_lazy('cc:solicitacoes')

    def get_context_data(self, **kwargs):
        """Adiciona form_title para ser usado nos templates"""
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context["form_title"] = 'Registre-se'
        return context

    def get_form_kwargs(self):
        """Passa request para logar automaticamente o usuario ao cadastrar-se"""
        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs
