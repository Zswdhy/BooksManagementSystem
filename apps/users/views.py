from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.users.models import Users
from apps.users.serializers import UserModelSerializers


class UserViewSets(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserModelSerializers
    authentication_classes = []
    permission_classes = []

    def update(self, request, *args, **kwargs):

        # 主键检验
        pk = self.kwargs.get("pk", 0)
        if not str(pk).isdigit():
            return Response({"code": "400", "message": "类型错误"}, status=status.HTTP_400_BAD_REQUEST)

        _user = self.queryset.filter(id=pk)
        if not _user:
            return Response({"code": "400", "message": "一个不存在的账号id."})

        # 修改用户密码
        data = self.request.data
        pwd = data.get("password", "")
        user = Users.objects.get(id=pk)

        if check_password(pwd, user.password):
            return Response({"code": "400", "message": "新密码不能和旧密码一样."})

        user.set_password(pwd)
        user.save()
        return Response({"code": 200, "message": "密码修改成功."})
