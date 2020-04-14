from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('signup/', views.signup_view, name="signup"),
    path('signup/', views.UserCreateView.as_view(), name="signup"),
    path('', views.UsersListView.as_view(), name='users'),
    path('<slug:slug>', views.UserDetailView.as_view(), name='user-detail'),
    path('<slug:slug>/update',
         views.UserUpdateView.as_view(), name='user-update'),

]
