from django.urls import path
from .views import oauth_connect, oauth_callback

urlpatterns = [
    path('connect/<str:provider>/', oauth_connect, name='oauth-connect'),
    path('callback/<str:provider>/', oauth_callback, name='oauth-callback'),
]
