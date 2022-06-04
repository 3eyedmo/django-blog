from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class TokenInvalid(APIException):
    status_code = 401
    default_detail = _('Token is Invalid')
    default_code = "invalid"