from ninja import Schema
from ninja import Form
from ninja_extra import ControllerBase
from ninja_extra import api_controller
from ninja_extra import route
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings

from django.contrib.auth.hashers import make_password


from core import schemas
from core import exceptions
from core.models import User

schema = SchemaControl(api_settings)


@api_controller("/auth", tags=["auth"])
class AuthController(ControllerBase):
    """Authentication controller."""

    auto_import = False

    @route.post(
        "/obtain",
        response=schema.obtain_pair_schema.get_response_schema(),
        url_name="auth_login",
    )
    def obtain_token(self, user_token: schema.obtain_pair_schema) -> type[Schema]:  # type: ignore
        """Get user's token.

        Args:
            user_token (schema.obtain_pair_schema): user's email and password.

        Returns:
            type[Schema]: jwt refresh and access token.
        """
        user_token.check_user_authentication_rule()
        return user_token.to_response_schema()

    @route.post(
        "/refresh",
        response=schema.obtain_pair_refresh_schema.get_response_schema(),
        url_name="auth_refresh_token",
    )
    def refresh_token(self, refresh_token: schema.obtain_pair_refresh_schema) -> type[Schema]:  # type: ignore
        """Refresh user's token.

        Args:
            refresh_token (schema.obtain_pair_refresh_schema): refresh token.

        Returns:
            type[Schema]: refresh and access token.
        """
        return refresh_token.to_response_schema()

    @route.post(
        "/verify",
        response={200: Schema},
        url_name="auth_verify_token",
    )
    def verify_token(self, token: schema.verify_schema) -> type[Schema]:  # type: ignore
        """Verify user's token.

        Args:
            token (schema.verify_schema): access token.

        Returns:
            type[Schema]: verify token.
        """
        return token.to_response_schema()

    @route.post(
        "/register",
        response={
            200: schemas.UserRigisterResponseSchema,
            400: schemas.Http400BadRequestSchema
        },
        url_name="auth_register",
    )
    def registe_user(self, body:Form[schemas.UserRigisterRequestSchema]):  # type: ignore
        """Register user."""
        if User.objects.filter(email=body.email).exists():
            raise exceptions.Http400BadRequestException("Email already exists")
        if body.password != body.password_confirm:
            raise exceptions.Http400BadRequestException("Password and confirm password must be the same")

        User.objects.create(
            email=body.email,
            password=make_password(body.password),
        )

        return {"email":body.email}
