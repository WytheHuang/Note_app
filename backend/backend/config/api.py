from django.http import HttpRequest
from ninja.openapi.docs import Redoc
from ninja_extra import NinjaExtraAPI
from note import apis as note_apis

from config.auth import AuthController


api = NinjaExtraAPI(
    title="Note App Backend",
    version="0.1.0",
    description="Note App in django",
    app_name="backend",
    docs=Redoc(),
    docs_url="docs/",
)


@api.get(
    "",
    tags=["health_check"],
)
async def api_root_health_check(request: HttpRequest):  # noqa: ARG001
    """Check api health."""
    return {"status": "healthy"}


@api.get(
    "health_check/",
    tags=["health_check"],
)
async def health_check(request: HttpRequest):  # noqa: ARG001
    """Check api health."""
    return {"status": "healthy"}


api.register_controllers(AuthController)

api.register_controllers(note_apis.NoteBookController)
