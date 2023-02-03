from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import Users


class UserModelSerializers(ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=Users.objects.all(),
            message={'message': '用户名重复'})
        ])

    def create(self, validated_data):
        user = Users.objects.create(**validated_data)
        user.set_password(validated_data.get("password"))
        user.type = "common"
        user.save()
        return user

    class Meta:
        model = Users
        fields = ["id", "username", "sex", "email", "type", "date_joined"]


class UserTestModelSerializers(ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "type", ]


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        print("user", user)
        token = super().get_token(user)
        print("token", token)
        token['name'] = user.username

        return token

    def validate(self, attrs):
        """
        登录返回token和refresh
        :param attrs:
        :return:
        """
        print(attrs["username"], attrs["password"])
        data = super().validate(attrs)
        print("data", data)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['token'] = str(data["access"])
        return data
