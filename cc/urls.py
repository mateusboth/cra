'''URLs do app cc'''
from django.urls import path
from . import views


app_name = 'cc'

urlpatterns = [
    # path('', views.index, name='index'),
    path('create/', views.SolicitacaoCreate.as_view(),
         name='solicitacao-create'),
    path('', views.SolicitacoesGenericList.as_view(), name='solicitacoes'),
    path('<slug:slug>', views.SolicitacoesGenericList.as_view(), name='solicitacoes'),
    # TODO arruma bagunça entre slug e pk pra ver do ano e detalhes
    path('<int:pk>', views.SolicitacaoDetailView.as_view(),
         name='solicitacao-detail'),
    # homologação
    path('<int:pk>/homologacao/',
         views.HomologacaoCreate.as_view(), name='homologacao-create'),
    path('<slug:slug>/homologacoes',
         views.HomologacaoFormSetView.as_view(), name="manage_homologacoes"),
    # ausentes
    path('<slug:slug>/ausentes',
         views.AusenteFormSetView.as_view(), name="manage_ausentes"),
    # Defini avaliadores
    path('<slug:slug>/avaliadores',
         views.AvaliadorFormSetView.as_view(), name="manage_avaliadores"),
    path('<int:pk_sol>/avaliador/<int:pk>',
         views.AvaliadorUpdate.as_view(), name='avaliador-update'),
    # resultado
    path('<int:pk_sol>/resultado/<int:pk>',
         views.ResultadoUpdate.as_view(), name='resultado-update'),
    # recurso
    path('<int:pk_sol>/resultado/<int:pk>/recurso/create',
         views.RecursoCreate.as_view(), name='recurso-create'),

]
