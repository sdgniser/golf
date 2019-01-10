from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.htm')),
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('p/<pid>/', views.problem_view, name='problem')
]
