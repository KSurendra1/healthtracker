from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.conf import settings
from .models import ExternalAccount
from .serializers import ExternalAccountSerializer
from .utils import revoke_external_account_tokens


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ExternalAccountViewSet(viewsets.GenericViewSet):
    serializer_class = ExternalAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExternalAccount.objects.filter(user=self.request.user)

    def list(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            obj = self.get_queryset().get(pk=pk)
        except ExternalAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            obj = self.get_queryset().get(pk=pk)
        except ExternalAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, obj)
        # Attempt to revoke tokens at the provider before deleting local record.
        try:
            revoked = revoke_external_account_tokens(obj)
        except Exception:
            revoked = False

        # If configured to fail when revocation fails, abort and return error
        if not revoked and getattr(settings, 'FAIL_REVOKE_ON_DISCONNECT', False):
            return Response({'detail': 'Failed to revoke provider token; aborting deletion.'}, status=status.HTTP_502_BAD_GATEWAY)

        # Otherwise proceed with local deletion regardless of revocation outcome
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
