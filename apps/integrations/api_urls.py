from rest_framework import routers
from django.urls import path, include
from .viewsets import ExternalAccountViewSet
from .views import ProvidersListAPIView

router = routers.DefaultRouter()
router.register(r'external-accounts', ExternalAccountViewSet, basename='externalaccount')

urlpatterns = [
    path('', include(router.urls)),
    path('providers/', ProvidersListAPIView.as_view(), name='integrations-providers'),
]
