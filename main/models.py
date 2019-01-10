from django.db import models

from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2000)

class Solution(models.Model):
    prob = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang = models.CharField(max_length=16)
    code = models.TextField(max_length=2000)
