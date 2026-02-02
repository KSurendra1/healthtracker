from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.device_id} ({self.owner})"
