'''URLs do app cc'''
from django.urls import path
from . import views


app_name = 'cc'

urlpatterns = [
    # path('', views.index, name='index'),
    path('solicitacao/create/', views.SolicitacaoCreate.as_view(),
         name='solicitacao-create'),
    path('solicitacoes', views.SolicitacoesGenericList.as_view(), name='solicitacoes'),
    path('solicitacao/<int:pk>', views.SolicitacaoDetailView.as_view(),
         name='solicitacao-detail'),
    #homologação
    path('solicitacao/<int:pk>/homologacao/',
         views.HomologacaoCreate.as_view(), name='homologacao-create'),
    #resultado
    path('solicitacao/<int:pk_sol>/resultado/<int:pk>',
         views.ResultadoUpdate.as_view(), name='resultado-update'),
    #recurso
    path('solicitacao/<int:pk_sol>/resultado/<int:pk>/recurso/create',
         views.RecursoCreate.as_view(), name='recurso-create'),
]
