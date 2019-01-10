from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm

from .models import *

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.is_valid()
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            base_url = reverse('home')
            query_string =  urlencode({'su': True})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
            #return HttpResponse('We have sent an email. Please confirm your email address to complete the registration')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.htm', {'form': form})

def index_view(request):
    prob_list = Problem.objects.all()
    return render(request, 'main/index.htm', {'p_list': prob_list})

def problem_view(request, pid):
    prob = Problem.objects.get(id=pid)
    return render(request, 'main/prob.html', {'p': prob})
