from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    steps = models.IntegerField(default=0)
    calories = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']

class HeartRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    bpm = models.IntegerField()
