from coreapi.compat import force_text
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from django.utils.translation import gettext_lazy as _


def _get_error_details(data, default_code=None):
    if isinstance(data, list):
        ret = [
            _get_error_details(item, default_code) for item in data
        ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: _get_error_details(value, default_code)
            for key, value in data.items()
        }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    text = force_text(data)
    code = getattr(data, 'code', default_code)
    return ErrorDetail(text, code)


class MyValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)
