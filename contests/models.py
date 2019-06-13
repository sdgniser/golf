from django.db import models
from django.utils.timezone import now

from django.contrib.auth import get_user_model

class Contest(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2000)
    start = models.DateTimeField()
    end = models.DateTimeField()
    winners = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.title

    def is_active(self):
        return (self.start <= now()
                and now() <= self.end)

    def is_upcoming(self):
        return self.start > now()

    def is_past(self):
        return self.end < now()

class Problem(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2000)
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def is_active(self):
        return self.contest.is_active()

    def is_past(self):
        return self.contest.is_past()

    def is_upcoming(self):
        return self.contest.is_upcoming()

class Solution(models.Model):
    prob = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lang = models.CharField(max_length=16)
    code = models.FileField(upload_to='code/')
    char_count = models.IntegerField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.prob) + ' by ' + str(self.user)
