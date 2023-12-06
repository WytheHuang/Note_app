from django.http import HttpRequest
from django.http.response import StreamingHttpResponse
from django.db.transaction import non_atomic_requests
from asgiref.sync import sync_to_async

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
@non_atomic_requests
async def api_check_helth(request: HttpRequest):
    return {"status": "healthy"}


api.register_controllers(AuthController)
