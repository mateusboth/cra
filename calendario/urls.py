from django.urls import path
from . import views

app_name = 'calendario'

urlpatterns = [
    path('', views.CalendarioListView.as_view(), name='calendarios'),
    path('create/', views.CalendarioCreate.as_view(), name='calendario-create'),
    path('<slug:slug>/', views.CalendarioDetailView.as_view(), name='calendario-detail'),
    path('<slug:slug>/update', views.CalendarioUpdate.as_view(), name='calendario-update'),
    path('<slug:slug>/delete', views.CalendarioDelete.as_view(), name='calendario-delete'),
]