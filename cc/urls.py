'''URLs do app cc'''
from django.urls import path
from . import views


app_name = 'cc'

urlpatterns = [
    # path('', views.index, name='index'),
    path('create/', views.SolicitacaoCreate.as_view(),
         name='solicitacao-create'),
    path('', views.SolicitacoesGenericList.as_view(), name='solicitacoes'),
    path('<int:pk>', views.SolicitacaoDetailView.as_view(),
         name='solicitacao-detail'),
    # homologação
    path('<int:pk>/homologacao/',
         views.HomologacaoCreate.as_view(), name='homologacao-create'),
    path('homologacoes/<slug:slug>',
         views.HomologacaoFormSetView.as_view(), name="manage_homologacoes"),
    # resultado
    path('<int:pk_sol>/resultado/<int:pk>',
         views.ResultadoUpdate.as_view(), name='resultado-update'),
    # recurso
    path('<int:pk_sol>/resultado/<int:pk>/recurso/create',
         views.RecursoCreate.as_view(), name='recurso-create'),

]
