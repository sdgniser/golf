from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from .views import *

app_name = 'contests'
urlpatterns = [
    path('', ActiveProblemList.as_view(), name='home'),
    path('p/active/', ActiveProblemList.as_view(), name='active'),
    path('p/past/', PastProblemList.as_view(), name='past'),
    path('p/future/', FutureProblemList.as_view(), name='future'),
    path('p/<pid>/', problem_detail, name='problem'),
    path('p/<pid>/leaderboard/', problem_leader_view, name='prob_leader'),

    path('leaderboard/', user_leader_view, name='user_leader'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
