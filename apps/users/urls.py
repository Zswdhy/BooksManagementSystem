from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.users.views import UserViewSets

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSets)

urlpatterns = [
    path("", include(router.urls)),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 系统自带
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify', TokenVerifyView.as_view(), name='token_verify'),
]
