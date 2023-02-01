from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.users.models import Users
from apps.users.serializers import UserModelSerializers


class TestAPIView(APIView):
    def get(self, request):
        return Response({"code": 200, "msg": "测试通过."})


class UserViewSets(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserModelSerializers
