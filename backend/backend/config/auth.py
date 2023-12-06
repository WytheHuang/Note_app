from ninja import Schema
from ninja_extra import ControllerBase
from ninja_extra import api_controller
from ninja_extra import route
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings


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
