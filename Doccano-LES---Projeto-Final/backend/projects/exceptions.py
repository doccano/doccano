from rest_framework import status
from rest_framework.exceptions import APIException


class RoleConstraintException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The project needs at least one administrator."


class RoleAlreadyAssignedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "This user is already assigned to a role in this project."
