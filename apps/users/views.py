from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import Users
from apps.users.serializers import UserModelSerializers, MyTokenObtainPairSerializer, UserTestModelSerializers


class TestAPIView(APIView):
    def get(self, request):
        return Response({"code": 200, "msg": "测试通过."})


class UserViewSets(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserModelSerializers
    authentication_classes = []
    permission_classes = []


class UserLoginAPIView(TokenObtainPairView):
    serializer_class = UserTestModelSerializers
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"code": "200", "data": serializer.data})
