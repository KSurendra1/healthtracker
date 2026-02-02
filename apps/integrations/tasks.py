from celery import shared_task
from django.contrib.auth import get_user_model
from .models import ExternalAccount


@shared_task
def trigger_initial_sync(user_id, provider):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    try:
        account = ExternalAccount.objects.get(user=user, provider=provider)
    except ExternalAccount.DoesNotExist:
        return

    # Placeholder: implement provider-specific sync logic here
    # e.g., enqueue per-day fetch jobs, call APIs with account.access_token
    return f"Triggered sync for {user.username} / {provider}"
