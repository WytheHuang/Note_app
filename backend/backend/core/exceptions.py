from ninja_extra import status
from ninja_extra.exceptions import APIException


class Http400BadRequestException(APIException):
    """base exception for Bad Request."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Bad Request"
    default_detail = "Bad Request"


class Http401UnauthorizedException(APIException):
    """base exception for Unauthorized."""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Unauthorized"
    default_detail = "Unauthorized"


class Http403ForbiddenException(APIException):
    """base exception for Forbidden."""

    status_code = status.HTTP_403_FORBIDDEN
    message = "Forbidden"
    default_detail = "Forbidden"


class Http404NotFoundException(APIException):
    """base exception for Not Found."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Not Found"
    default_detail = "Not Found"
