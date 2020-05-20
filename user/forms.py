from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from curso.models import Curso
User = get_user_model()


class SignUpForm(UserCreationForm):
    """Form para cadastro de novos usuários"""
    class Meta:
        model = User
        fields = ('nome_completo', 'matricula', 'curso',
                  'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        """Filtra apenas os cursos ativos"""
        request = kwargs.pop('request')
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['curso'].queryset = Curso.objects.filter(is_active=True)
        self.instance.request = request

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            auth_user = authenticate(
                username=self.cleaned_data['matricula'],
                password=self.cleaned_data['password1']
            )
            login(self.instance.request, auth_user) # efetua login
        return user
