from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Curso, Disciplina
# Create your views here.


class CursoCreate(SuccessMessageMixin, CreateView):
    model = Curso
    fields = ('nome', 'abreviacao', 'matriz', 'is_active')
    # permission_required = 'user.staff'
    template_name = 'create_form_generic.html'
    success_url = reverse_lazy('curso:cursos')
    success_message = 'Curso adicionado com sucesso'

    def get_context_data(self, **kwargs):
        """Adiciona form_title para ser usado nos templates"""
        context = super().get_context_data(**kwargs)
        context["form_title"] = 'Adicionar novo Curso'
        return context

class CursoUpdate(SuccessMessageMixin, UpdateView):
    model = Curso
    fields = ('nome', 'abreviacao', 'matriz', 'is_active')
    # permission_required = 'user.staff'
    template_name = 'create_form_generic.html'
    success_message ='Curso editado com sucesso'

    def get_context_data(self, **kwargs):
        """Adiciona form_title para ser usado nos templates"""
        context = super().get_context_data(**kwargs)
        context["form_title"] = 'Editar Curso'
        return context

class CursoDelete(DeleteView):
    model = Curso
    success_url = reverse_lazy('curso:cursos')
    #permission_required = 'staff'
    success_message = 'Curso deletado com sucesso'

    def delete(self, request, *args, **kwargs):
        """Mensagem  de sucesso ao deletar"""
        super(CursoDelete, self).delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

class CursosListView(ListView):
    """Generic class-based view for a list of cursos."""
    model = Curso
    paginate_by = 15
    # permission_required = 'user.staff'


class CursoDetailView(DetailView):
    """Generic class-based detail view for a curso."""
    model = Curso
    # permission_required = 'user.staff'

# Disciplinas

# class DisciplinaCreate(PermissionRequiredMixin, CreateView):
#     '''Cria disciplina, exigi perms.user.staff'''
#     model = Disciplina
#     fields = ['codigo', 'nome', 'curso', 'semestre']
#     permission_required = 'user.staff'
#     template_name = 'create_form_generic.html'

# class DisciplinaUpdate(PermissionRequiredMixin, UpdateView):
#     Model = Disciplina
#     fields = '__all__'
#     permission_required = 'user.staff'

class DisciplinasGenericList(ListView):
    '''Lista de todas as disciplinas'''
    model = Disciplina
    paginate_by = 50
    # permission_required = 'user.staff'


class DisciplinaDetailView(DetailView):
    '''Detalhes da disciplinas especifica'''
    model = Disciplina
    # permission_required = 'user.staff'
