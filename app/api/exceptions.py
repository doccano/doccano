from rest_framework import status
from rest_framework.exceptions import APIException


class FileParseException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid file format, line {}: {}'
    default_code = 'invalid'

    def __init__(self, line_num, line, code=None):
        detail = self.default_detail.format(line_num, line)
        super().__init__(detail, code)


class AutoLabelingException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Auto labeling not allowed for the document with labels.'
