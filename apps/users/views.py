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

    def get1(self, request):
        essay = self.request.data.get("essay")
        ans = []
        paragraph = 1
        sentence = 1
        for item in essay.split("\n"):
            temp = {}
            item = item.strip()
            if len(item) != 0:
                temp["paragraph"] = paragraph
                paragraph += 1
                temp["paragraph_text"] = item
                # _temp = item.replace("Mr.", "Mr零").replace("Mrs.", "Mrs零").replace("Dr.", "Dr零").replace("Ms.", "Ms零") \
                #     .replace("?", "?。").replace(".", ".。").replace("!", "!。").replace("零", ".").split("。")
                for _item in re.split(r'(\w+)|(’\w+)|(,)|(”)|(\?)|(!)', item):
                    if _item is not None:
                        print('word', _item, type(_item))
                _temp = item.replace('. ', '.零').replace("?", "?。").replace("!", "!。").replace("“ ", "”零").split("零")
                sents = []
                for sent in _temp:
                    sent = sent.strip()
                    if sent:
                        word_details = []
                        word_index = 1

                        for item in re.split(r"\s", sent):
                            item = item.strip()
                            if item == "":
                                continue
                            elif ord(item[-1]) == 8221:

                                if re.search(r'[a-z|A-Z|0-9]', item[-2]):
                                    word_details.append({'word': item[:-1], "word_index": word_index})
                                    word_index += 1
                                else:
                                    word_details.append({'word': item[:-2], "word_index": word_index})
                                    word_index += 1
                                    word_details.append({'word': item[-2], "word_index": word_index})
                                    word_index += 1
                                word_details.append({'word': '“', "word_index": word_index})
                                word_index += 1
                            elif item[-1] == '.':
                                if ")" in item:
                                    left = item.split(")")[0]
                                    word_details.append({'word': left, "word_index": word_index})
                                    word_index += 1
                                    word_details.append({'word': ")", "word_index": word_index})
                                    word_index += 1
                                    word_details.append({'word': '.', "word_index": word_index})
                                    word_index += 1
                                else:
                                    word_details.append({'word': item[:-1], "word_index": word_index})
                                    word_index += 1
                                    word_details.append({'word': '.', "word_index": word_index})
                                    word_index += 1
                            elif item[-1] == '?':
                                word_details.append({'word': item[:-1], "word_index": word_index})
                                word_index += 1
                                word_details.append({'word': '?', "word_index": word_index})
                                word_index += 1
                            elif item[-1] == ',':
                                word_details.append({'word': item[:-1], "word_index": word_index})
                                word_index += 1
                                word_details.append({'word': ',', "word_index": word_index})
                                word_index += 1
                            elif "'" in item:
                                left, right = item.split("'")[0], item.split("'")[1]
                                word_details.append({'word': left, "word_index": word_index})
                                word_index += 1
                                word_details.append({'word': "'" + right, "word_index": word_index})
                                word_index += 1
                            elif "(" in item:
                                right = item.split("(")[1]
                                word_details.append({'word': "(", "word_index": word_index})
                                word_index += 1
                                word_details.append({'word': right, "word_index": word_index})
                                word_index += 1
                            elif ")" in item:
                                left = item.split(")")[0]
                                word_details.append({'word': left, "word_index": word_index})
                                word_index += 1
                                word_details.append({'word': ")", "word_index": word_index})
                                word_index += 1
                            elif "“" in item:
                                left, right = item.split('“')[0], item.split('“')[1]
                                if left:
                                    word_details.append({'word': right, "word_index": word_index})
                                    word_index += 1
                                    word_details.append({'word': '“', "word_index": word_index})
                                    word_index += 1

                                else:
                                    word_details.append({'word': '“', "word_index": word_index})
                                    word_index += 1
                                    word_details.append({'word': right, "word_index": word_index})
                                    word_index += 1

                            else:
                                word_details.append({'word': item, "word_index": word_index})
                                word_index += 1
                        sents.append({"sentence": sentence, "sentence_text": sent, "word": word_details})

                        sentence += 1
                temp["sentence_details"] = sents

                ans.append(temp)
        return Response({"code": 200, "data": ans})

    def get(self, request):

        def split_sentence(sentence):
            word = []
            word_idx = 1
            for item in re.split(r'(\w+)|(’\w+)|(,)|(”)|(\?)|(!)', sentence):
                if isinstance(item, str) and len(item.strip()) > 0:
                    word.append({'word': item, 'word_idx': word_idx})
                    word_idx += 1
            return word

        essay = self.request.data.get("essay")
        ans = []
        para_idx = 1
        sent_idx = 1
        for item in essay.split("\n"):
            temp = {}
            item = item.strip()
            if len(item) != 0:
                temp["para"] = para_idx
                para_idx += 1
                temp["para_text"] = item
                para_ls = []
                para_data = list(filter(lambda x: isinstance(x, str), re.split(r'(\.\s+)|(\.”)', item)))

                if len(para_data) == 1:
                    temp["para_details"] = [
                        {'sent': para_data[0], "sent_idx": sent_idx,
                         "sent_details": split_sentence(para_data[0].strip())}]
                    sent_idx += 1
                    ans.append(temp)
                    continue

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
                ans.append(temp)

        return Response({"code": 200, "data": ans})
