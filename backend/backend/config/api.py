from ninja_extra import NinjaExtraAPI

from config.auth import AuthController


api = NinjaExtraAPI(
    title="Note App Backend",
    version="0.1.0",
    description="Note App in django",
    app_name="backend",
)


api.register_controllers(AuthController)
