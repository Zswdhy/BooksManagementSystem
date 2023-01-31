from django.urls import path, include

from apps.users.views import TestAPIView

urlpatterns = [
    path("test", TestAPIView.as_view())
]
