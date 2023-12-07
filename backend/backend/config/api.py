from django.http import HttpRequest
from ninja.openapi.docs import Redoc
from ninja_extra import NinjaExtraAPI

from config.auth import AuthController


api = NinjaExtraAPI(
    title="Note App Backend",
    version="0.1.0",
    description="Note App in django",
    app_name="backend",
    docs=Redoc(),
    docs_url="/docs",
)


@api.get("/")
async def api_check_helth(request: HttpRequest):  # noqa: ARG001
    """Check api health."""
    return {"status": "healthy"}


api.register_controllers(AuthController)
