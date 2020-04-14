from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from .models import User
from curso.models import Curso
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
User = get_user_model()

# Create your views here.

@login_required
def home(request):
    users =  User.objects.all()
    num_user = users.count()
    context = {
        'users': users,
        'num_user': num_user
        }
    print(f'context: {context}')

    return render(
        request, 'home.html', context=context
    )

# def signup_view(request):
#     if request.method  == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             matricula = form.cleaned_data.get('matricula')
#             user.curso = form.cleaned_data.get('curso')
#             password = form.cleaned_data.get('password1')
#             user.nome_completo = form.cleaned_data.get('nome_completo')
#             user.email = form.cleaned_data.get('email') 
#             user = authenticate(username=matricula, password=password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})

class UserCreateView(CreateView):
    template_name = 'create_form_generic.html'
    form_class = SignUpForm
    
    def get_context_data(self, **kwargs):
        """Adiciona form_title para ser usado nos templates"""
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context["form_title"] = 'Registre-se'
        return context

class UsersListView(PermissionRequiredMixin, generic.ListView):
    model = User
    fields = '__all__'
    permission_required = 'user.staff'

class UserDetailView(PermissionRequiredMixin, generic.DetailView):
    model = User
    fields = '__all__'
    context_object_name = 'usuario'
    permission_required = 'user.staff'

class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    fields = '__all__'
    context_object_name = 'usuarios'
    permission_required = 'user.staff'
    template_name = 'create_form_generic.html'