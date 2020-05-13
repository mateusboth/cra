from django.urls import path
from . import views


app_name = 'relatorio'

urlpatterns = [
    path('<slug:slug>/homologado/', views.HomologadoPdfView.as_view(), name='homologado-pdf'),
    path('<slug:slug>/resultado/', views.ResultadoPdfView.as_view(), name='resultado-pdf'),  
    path('<slug:slug>/ficha-individual/', views.FichaIndividualPdfView.as_view(), name='ficha-individual-pdf'),  
    path('<slug:slug>/folha-rosto/', views.FolhaRostoPdfView.as_view(), name='folha-rosto-pdf'),  
]