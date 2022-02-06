from rest_framework import status
from rest_framework.exceptions import APIException


class LabelValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You cannot create a label with same name or shortcut key."
