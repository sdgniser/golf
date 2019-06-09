from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Problem(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2000)

    def __str__(self):
        return self.title

class Solution(models.Model):
    prob = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lang = models.CharField(max_length=16)
    code = models.FileField(upload_to='code/')
    char_count = models.IntegerField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.prob) + ' by ' + str(self.user)
