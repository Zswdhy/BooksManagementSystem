from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    sex = models.BooleanField(default=True, verbose_name="性别")  # 默认男性
    type = models.CharField(max_length=16, default="", verbose_name="用户权限")  # root、admin、common

    class Meta:
        db_table = "用户表"
