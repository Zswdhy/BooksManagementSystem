from django.urls import path, include
from rest_framework import routers

from apps.users.views import TestAPIView, UserViewSets

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSets)

urlpatterns = [
    path("", include(router.urls)),
    path("test", TestAPIView.as_view()),
]
