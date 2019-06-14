from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import DetailView, ListView

from .forms import *
from .models import *


class ProblemList(ListView):
    model = Problem
    template_name = 'prob_list.htm'
    all_states = ['active', 'future', 'past']
    state = 'active'
    context_object_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_states'] = self.all_states
        context['state'] = self.state
        return context

class ActiveProblemList(ProblemList):
    state = 'active'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['probs'] = Problem.objects.filter(start__lt = now(),
                end__gt = now())
        return context

class PastProblemList(ProblemList):
    state = 'past'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['probs'] = Problem.objects.filter(end__lt = now())
        return context

class FutureProblemList(ProblemList):
    state = 'future'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['probs'] = Problem.objects.filter(start__gt = now()) 
        return context

def problem_detail(request, pid):
    """
    Displays the problem. Provides a form to record the solution if a user is
    logged in. Accepts a UTF-8 encoded plaintext file as solution.
    """
    prob = Problem.objects.get(id=pid)

    if prob.is_upcoming():
        raise Http404('Problem not out yet.')

    if request.method == 'POST':
        # Throws an error if a POST request is received for a problem that is
        # not active
        if not prob.is_active():
            messages.error(request, 'The problem you tried to submit a \
            solution for is not active at this time.')
            return HttpResponseRedirect(reverse('contests:home'))

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
                return HttpResponseRedirect(reverse('contests:problem', 
                    args=(pid,)))

            # Everything went nicely!
            messages.success(request, 'Your solution has been recorded\
            successfully. It will appear in the leaderboard once it is\
            verified to be working by one of the moderators.')
            return HttpResponseRedirect(reverse('contests:home'))

    # Stuff to do for a GET request
    else:
        form = None
        repeat_submission = False
        # Display a submission form only if the user is authenticated and the
        # problem is active
        if request.user.is_authenticated and prob.is_active():
            form = SolutionForm()
            if Problem.objects.filter(id=pid, solution__user=request.user):
                repeat_submission = True
                form = None

    return render(request, 'prob_detail.htm', {'p': prob, 's_form': form,
                    'repeat_submission': repeat_submission,})

def problem_leader_view(request, pid):
    prob = Problem.objects.get(id=pid)
    ranked_solutions = Solution.objects.filter(prob=prob,
            is_correct=True).order_by('char_count', 'sub_time')

    return render(request, 'prob_leader.htm', {'prob': prob, 'solns':
        ranked_solutions})
