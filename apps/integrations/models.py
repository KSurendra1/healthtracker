from django.db import models
from django.contrib.auth.models import User

class ExternalAccount(models.Model):
    PROVIDER_CHOICES = (
        ('fitbit', 'Fitbit'),
        ('googlefit', 'Google Fit'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=32, choices=PROVIDER_CHOICES)
    provider_user_id = models.CharField(max_length=128)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'provider')
