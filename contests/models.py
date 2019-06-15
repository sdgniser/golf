from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from dirtyfields import DirtyFieldsMixin

from statistics import mean, stdev
from math import tanh

from .helpers import gen_file_name

class Problem(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2000)
    base_score = models.IntegerField(default=10)
    start = models.DateTimeField(default=now())
    end = models.DateTimeField(default=now())

    def __str__(self):
        return self.title

    def is_active(self):
        return (self.start <= now() and now() <= self.end)

    def is_past(self):
        return self.end < now()

    def is_upcoming(self):
        return self.start > now()

    def leader(self):
        ranked_leaders = get_user_model().objects.filter(solution__prob=self,
                solution__is_correct=True).order_by('solution__char_count',
                        'solution__sub_time')
        if ranked_leaders:
            return ranked_leaders[0]


class Solution(DirtyFieldsMixin, models.Model):
    prob = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lang = models.CharField(max_length=16)
    code = models.FileField(upload_to=gen_file_name)
    char_count = models.IntegerField()
    sub_time = models.DateTimeField(default=now())
    is_correct = models.BooleanField(default=False)

    FIELDS_TO_CHECK = ['is_correct']

    def __str__(self):
        return str(self.prob) + ' by ' + str(self.user)

    def avg_char_count(self, prob):
        return Solution.objects.filter(prob=prob,
                is_correct=True).aggregate(Avg('char_count'))

    def calc_score(self, MULT=3):
        prob = Problem.objects.get(id=self.prob.id)
        all_soln = Solution.objects.filter(is_correct=True, prob=prob)

        char_count = self.char_count
        char_count_array = []
    
        for s in all_soln:
            char_count_array += [s.char_count]
    
        avg_char_count = 0 
        sd_char_count = 0.01 # Aah! Magic constant! AAAAH!
        if len(char_count_array) > 1:
            avg_char_count = mean(char_count_array)
            sd_char_count = stdev(char_count_array)
    
        mult = 1 + (MULT/2) + (MULT/2)*tanh((char_count - avg_char_count)
                                                              / sd_char_count)
        return round(prob.base_score * mult, 0)

    def save(self, *args, **kwargs):
        score = self.calc_score()
        dirty = self.is_dirty()
        super().save(*args, **kwargs)

        if self.is_correct and dirty:
            self.user.score += score
            self.user.save()
