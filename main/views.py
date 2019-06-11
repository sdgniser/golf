from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import *

def index_view(request):
    prob_list = Problem.objects.all()
    return render(request, 'index.htm', {'p_list': prob_list})

def problem_view(request, pid):
    """
    Displays the problem. Provides a form to record the solution if a user is
    logged in. Accepts a UTF-8 encoded plaintext file as solution.
    """
    prob = Problem.objects.get(id=pid)

    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            code = form.cleaned_data['code']

            codefile = code.read()
            try:
                char_count = len(codefile.decode('utf-8', 'strict'))

                # Creating the Solution object
                Solution.objects.create(prob=prob, user=request.user,
                        lang=form.cleaned_data['lang'], code=code,
                        char_count=char_count)
             
            # Throws a hissy fit if it doesn't like the uploaded file
            except UnicodeDecodeError:
                messages.error(request, 'The file you uploaded could not be\
                processed by the backend. It only accepts UTF-8 encoded\
                plaintext files.')
                return HttpResponseRedirect(reverse('main:problem', 
                    args=(pid,)))

            # If the following two commands execute everything went nicely.
            messages.success(request, 'Your solution has been recorded\
            successfully. It will appear in the leaderboard once it is\
            verified to be working by one of the moderators.')
            return HttpResponseRedirect(reverse('main:home'))

    # Stuff to do for a GET request
    else:
        # Don't display the form if the user has already
        # submitted a solution
        form = None
        if request.user.is_authenticated:
            form = SolutionForm()
            if Problem.objects.filter(solution__user=request.user):
                form = None

    return render(request, 'prob.htm', {'p': prob, 's_form': form,})

def leader_view(request, pid):
    prob = Problem.objects.get(id=pid)
    solns = Solution.objects.order_by('char_count').filter(prob__id=pid,
            is_correct=True)

    return render(request, 'prob_leader.htm', {'p': prob, 's_list': solns})
