from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name="signup"),
    path('users/', views.UsersListView.as_view(), name='users'),
    path('user/<slug:slug>', views.UserDetailView.as_view(), name='user-detail'),
    path('user/<slug:slug>/update',
         views.UserUpdateView.as_view(), name='user-update'),

]
