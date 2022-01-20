from rest_framework import status
from rest_framework.exceptions import APIException


class FileParseException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid file format, line {}: {}'
    default_code = 'invalid'

    def __init__(self, line_num, line, code=None):
        detail = self.default_detail.format(line_num, line)
        super().__init__(detail, code)


class LabelValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot create a label with same name or shortcut key.'


class AnnotationRelationValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot create an annotation relation between the same annotation.'


class RelationTypesValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot create a relation type with same name or color.'
