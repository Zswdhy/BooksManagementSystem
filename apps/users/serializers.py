from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

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
        fields = ["id", "username", "sex", "password", "email", "type", "date_joined"]
        extra_kwargs = {"password": {"write_only": True}}


class UserTestModelSerializers(ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "type", ]
