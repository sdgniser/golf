from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model. Flexible.
    """
    
    username = models.CharField(max_length=150, primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.username})
