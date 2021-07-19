from rest_framework import status
from rest_framework.exceptions import (APIException, PermissionDenied,
                                       ValidationError)


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


class AutoLabelingPermissionDenied(PermissionDenied):
    default_detail = 'You do not have permission to perform auto labeling.' \
                     'Please ask the project administrators to add you.'


class URLConnectionError(ValidationError):
    default_detail = 'Failed to establish a connection. Please check the URL or network.'


class AWSTokenError(ValidationError):
    default_detail = 'The security token included in the request is invalid.'


class SampleDataException(ValidationError):
    default_detail = 'The response is empty. Maybe the sample data is not appropriate.' \
                     'Please specify another sample data which returns at least one label.'


class TemplateMappingError(ValidationError):
    default_detail = 'The response cannot be mapped. You might need to change the template.'


class LabelValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot create a label with same name or shortcut key.'


class AnnotationRelationValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot create an annotation relation between the same annotation.'


class RelationTypesValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot create a relation type with same name or color.'


class RoleConstraintException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The project needs at least one administrator.'


class RoleAlreadyAssignedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This user is already assigned to a role in this project.'
