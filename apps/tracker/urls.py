from rest_framework import routers
from .views import ActivityViewSet, HeartRateViewSet

router = routers.DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'heartrate', HeartRateViewSet)

urlpatterns = router.urls
