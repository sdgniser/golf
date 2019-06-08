from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView


from .models import *

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'main/signup.htm'

def index_view(request):
    prob_list = Problem.objects.all()
    return render(request, 'main/index.htm', {'p_list': prob_list})

def problem_view(request, pid):
    prob = Problem.objects.get(id=pid)
    return render(request, 'main/prob.htm', {'p': prob})
