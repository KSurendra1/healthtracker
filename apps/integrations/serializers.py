from rest_framework import serializers
from .models import ExternalAccount

class ExternalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalAccount
        fields = ('id', 'provider', 'provider_user_id', 'expires_at')
        read_only_fields = ('id', 'provider', 'provider_user_id', 'expires_at')
