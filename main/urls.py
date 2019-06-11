from django.urls import path, include

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index_view, name='home'),
    path('p/<pid>/', views.problem_view, name='problem'),
    path('leaderboard/p/<pid>/', views.leader_view, name='leaderboard'),
]
