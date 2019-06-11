from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import CustomUserCreationForm
from main.models import *

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'signup.htm'

class UserView(DetailView):
    model = get_user_model()
    template_name = 'user.htm'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """
        Adds the following to the context:
        * List of problems solved by the user: p_list
        * List of languages used: langs
        * Total character count across all solutions: total_count
        * Character count per solution submitted: avg_count
        """
        context = super().get_context_data(**kwargs)
        current_user = context['user']

        # Gets the list of problems solved correctly
        p_list = Problem.objects.filter(solution__is_correct=True,
                solution__user=current_user)
        context['p_list'] = p_list

        # Logic to get list of programming languages used
        solns = Solution.objects.filter(user=current_user)
        langs = []
        for soln in solns:
            if soln.lang not in langs:
                langs.append(soln.lang)

        context['langs'] = langs

        # Logic for total and average character count
        if not solns:
            return context

        total_count = 0
        for soln in solns:
            total_count += soln.char_count

        avg_count = total_count // len(solns)
        context['total_count'] = total_count
        context['avg_count'] = avg_count

        return context
