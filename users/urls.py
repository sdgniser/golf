from django.contrib.auth.views import LoginView
from django.urls import path, include

from .views import *

app_name = 'users'
urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='login.htm')),
    path('', include('django.contrib.auth.urls')),
    path('<slug:pk>', UserView.as_view(), name='profile'),
]
