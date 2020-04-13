from django.urls import path
from . import views

app_name = 'curso'
urlpatterns = [
    path('', views.CursosListView.as_view(), name='cursos'),
    path('create/', views.CursoCreate.as_view(), name='curso-create'),
    path('<slug:slug>/update/', views.CursoUpdate.as_view(), name='curso-update'),
    path('<slug:slug>/delete/', views.CursoDelete.as_view(), name='curso-delete'),
    path('<slug:slug>/', views.CursoDetailView.as_view(), name='curso-detail'),
    #disciplinas
    # path('disciplina/create/', views.DisciplinaCreate.as_view(), name='disciplina-create'),
    path('disciplinas', views.DisciplinasGenericList.as_view(), name='disciplinas'),
    path('disciplina/<slug:slug>', views.DisciplinaDetailView.as_view(), name='disciplina-detail'),
    # path('disciplina/<slug:slug>/update/', views.DisciplinaUpdate.as_view(), name='disciplina-update'),
]

