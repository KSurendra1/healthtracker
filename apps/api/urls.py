from django.urls import path, include
from rest_framework import routers
from apps.tracker.urls import router as tracker_router

router = routers.DefaultRouter()

# Include tracker routers under api/
urlpatterns = [
    path('', include((tracker_router.urls, 'tracker'))),
    path('accounts/', include('apps.accounts.urls')),
    path('integrations/', include('apps.integrations.urls')),
    path('integrations-api/', include('apps.integrations.api_urls')),
    path('devices/', include('apps.devices.urls')),
]
