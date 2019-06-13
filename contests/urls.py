from django.urls import path, include

from .views import *

app_name = 'contests'
urlpatterns = [
    path('', ActiveContestList.as_view(), name='home'),
    path('problem/<pid>/', problem_view, name='problem'),

    path('contests/all/', ContestList.as_view(), name='all'),
    path('contests/active/', ActiveContestList.as_view(), name='active'),
    path('contests/past/', PastContestList.as_view(), name='past'),
    path('contests/future/', FutureContestList.as_view(), name='future'),

    path('contest/<int:pk>', ContestDetail.as_view(), name='contest'),

    path('leaderboard/p/<pid>/', leader_view, name='prob_leader'),
]
