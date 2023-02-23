import re

from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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


class TestSimpleJwt(APIView):

    def get(self, request):
        return Response({"code": "200", "message": "simple jwt 校验成功"})


class EssayPretreatment(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        def split_essay(item, sent_idx):
            temp = {}
            temp["para_text"] = item
            para_ls = []
            para_data = list(filter(lambda x: isinstance(x, str), re.split(r'(\.\s+)|(\.”)', item)))

            if len(para_data) == 1:
                temp["para_details"] = [
                    {'sent': para_data[0], "sent_idx": sent_idx,
                     "sent_details": split_sentence(para_data[0].strip())}]
                sent_idx += 1
                return temp, sent_idx

            left = 0
            i = 0
            while i < len(para_data):
                cur_text = para_data[i].strip()
                if cur_text in ['.', '.”']:
                    if para_data[i - 1].split()[-1] in ["Mr", "Mrs", "Dr", "Ms"] or \
                            len(para_data[i - 1].split()[-1]) == 1:

                        for j in range(i + 1, len(para_data)):
                            if para_data[j].strip() in ['.', '.”']:
                                i = j
                                break

                        para_ls.append(
                            {'sent': ''.join(para_data[left:i + 2]), 'sent_idx': sent_idx,
                             "sent_details": split_sentence(''.join(para_data[left:i + 2]).strip())})
                        sent_idx += 1
                        left = i + 2
                        i += 2
                    else:
                        para_ls.append({'sent': ''.join(para_data[left:i + 1]), 'sent_idx': sent_idx,
                                        "sent_details": split_sentence(''.join(para_data[left:i + 1]).strip())})
                        sent_idx += 1
                        left = i + 1
                        i += 1
                else:
                    i += 1

            temp["para_details"] = para_ls
            return temp, sent_idx

        def split_sentence(sentence):
            word = []
            word_idx = 1

            word_data = list(filter(lambda x: isinstance(x, str) and len(x.strip()) > 0,
                                    re.split(r'(\w+)|(’\w+)|(,)|(”)|(\?)|(!)', sentence)))
            i = 0
            while i < len(word_data):
                # 需要考虑\d\.\d、Mr\.+\w 情况
                _type = isinstance(word_data[i], str)
                if not _type or _type and len(word_data[i].strip()) <= 0:
                    i += 1
                    continue
                if word_data[i] in ["Mr", "Mrs", "Dr", "Ms"] and word_data[i + 1].strip() == '.':
                    word.append({"word": ''.join(word_data[i:i + 3]), "word_idx": word_idx})
                    word_idx += 1
                    i += 3
                elif word_data[i].isdigit() and word_data[i + 1].strip() == '.' and word_data[i + 2].isdigit():
                    word.append({"word": ''.join(word_data[i:i + 3]), "word_idx": word_idx})
                    word_idx += 1
                    i += 3

                elif word_data[i] == "'" and word_data[i + 1].isalpha():
                    word.append({"word": ''.join(word_data[i:i + 2]), "word_idx": word_idx})
                    word_idx += 1
                    i += 2
                else:
                    word.append({'word': word_data[i], 'word_idx': word_idx})
                    word_idx += 1
                    i += 1

            return word

        essay = self.request.data.get("essay")
        ans = []
        para_idx = 1
        sent_idx = 1
        for item in essay.split("\n"):
            item = item.strip()
            if len(item) == 0:
                continue

            temp, sent_idx = split_essay(item, sent_idx)
            temp["para_idx"] = para_idx
            para_idx += 1
            ans.append(temp)

        return Response({"code": 200, "data": ans})
