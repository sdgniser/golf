from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import CustomUserCreationForm
from main.models import *

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'main/signup.htm'

class UserView(DetailView):
    model = get_user_model()
    template_name = 'main/user.htm'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = context['user']

        # Logic to get list of problems solved
        probs = Problem.objects.filter(solution__is_correct=True,
                solution__user=current_user)
        p_list_dummy = []
        p_list = []
        for prob in probs:
            if prob.title not in p_list_dummy:
                p_list.append(prob)
                p_list_dummy.append(prob.title)
        
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
