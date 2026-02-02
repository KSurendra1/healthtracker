from rest_framework import viewsets, permissions
from .models import Activity, HeartRate
from .serializers import ActivitySerializer, HeartRateSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

class HeartRateViewSet(viewsets.ModelViewSet):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer
    permission_classes = [permissions.IsAuthenticated]
