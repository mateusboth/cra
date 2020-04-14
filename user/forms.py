from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from curso.models import Curso
User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('nome_completo', 'matricula', 'curso',
                  'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        """Filtra apenas os cursos ativos"""
        super(SignUpForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['curso'].queryset = Curso.objects.filter(is_active=True)
    
    
