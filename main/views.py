from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import *
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

    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            code = form.cleaned_data['code']

            # Logic to count the number of characters in the file
            codefile = code.read()
            char_count = len(codefile.decode('utf-8', 'strict'))

            # Creating the Solution object
            Solution.objects.create(prob=prob, user=request.user,
                    lang=form.cleaned_data['lang'], code=code,
                    char_count=char_count)

            return HttpResponseRedirect(reverse('home'))

    else:
        form = SolutionForm()

    return render(request, 'main/prob.htm', {'p': prob, 's_form': form,})

def leader_view(request, pid):
    prob = Problem.objects.get(id=pid)
    solns = Solution.objects.order_by('char_count').filter(prob__id=pid,
            is_correct=True)

    return render(request, 'main/prob_leader.htm', 
            {'p': prob, 's_list': solns})
