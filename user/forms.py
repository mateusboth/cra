from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    nome_completo = forms.CharField(max_length=70)
    matricula = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('nome_completo', 'matricula', 'curso', 'email', 'password1', 'password2', )