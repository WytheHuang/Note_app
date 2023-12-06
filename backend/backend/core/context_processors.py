from django.conf import settings
from rest_framework.request import Request


def allauth_settings(request: Request) -> dict[str, bool]:  # noqa: ARG001
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }
