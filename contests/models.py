from django.db import models
from django.utils.timezone import now

from django.contrib.auth import get_user_model

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

#     def leader_list(self):
#         ranked_leaders = get_user_model().objects.filter(solution__prob=self,
#                 solution__is_correct=True).order_by('solution__char_count',
#                         'solution__sub_time')
#         leader_dict = {}
#         for person in ranked_leaders:
#             leader_dict[person] = Solution.objects.get(user=person)
# 
#         return leader_dict


class Solution(models.Model):
    prob = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lang = models.CharField(max_length=16)
    code = models.FileField(upload_to='code/')
    char_count = models.IntegerField()
    sub_time = models.DateTimeField(default=now())
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.prob) + ' by ' + str(self.user)
