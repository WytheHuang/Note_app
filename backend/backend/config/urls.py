from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.handlers.asgi import ASGIRequest
from django.shortcuts import redirect
from django.urls import include
from django.urls import path
from django.views import defaults as default_views

from .api import api


def redirect_to_admin(request: ASGIRequest):  # noqa: ARG001
    """Redirect to admin.

    Args:
        request (ASGIRequest): request
    """
    return redirect("admin/")


urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("admin/", admin.site.urls),
    #
    path("", redirect_to_admin),
    #
    path("accounts/", include("allauth.urls")),
    #
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    #
    path("api/", api.urls, name="api_root"),  # type: ignore
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
