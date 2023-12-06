from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


if typing.TYPE_CHECKING:
    from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):  # noqa: D101
    def is_open_for_signup(self: AccountAdapter, request: HttpRequest) -> bool:  # noqa: ARG002, D102
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


# social account adapter
# class SocialAccountAdapter(DefaultSocialAccountAdapter):
#     def is_open_for_signup(self, request: HttpRequest, sociallogin: SocialLogin) -> bool:
#         return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

#     def populate_user(self, request: HttpRequest, sociallogin: SocialLogin, data: dict[str, typing.Any]) -> User:
#         """
#         Populates user information from social provider info.

#         See: https://django-allauth.readthedocs.io/en/latest/advanced.html?#creating-and-populating-user-instances
#         """
#         user = sociallogin.user
#         if name := data.get("name"):
#             user.name = name
#         elif first_name := data.get("first_name"):
#             user.name = first_name
#             if last_name := data.get("last_name"):
#                 user.name += f" {last_name}"
#         return super().populate_user(request, sociallogin, data)
