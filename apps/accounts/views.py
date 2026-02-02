from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
