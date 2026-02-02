from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=64, default='UTC')
    country = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
