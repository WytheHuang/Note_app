from ninja import Schema


class Http400BadRequestSchema(Schema):
    """Base schema for 400 response."""

    detail: str = "Bad Request"


class Http401UnauthorizedSchema(Schema):
    """Base schema for 401 response."""

    detail: str = "Unauthorized"


class Http403ForbiddenSchema(Schema):
    """Base schema for 403 response."""

    detail: str = "Forbidden"


class Http404NotFoundSchema(Schema):
    """Base schema for 404 response."""

    detail: str = "Not Found"


class BaseResponseSchema(Schema):
    """Base schema for response."""

    msg: str
