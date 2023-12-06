from typing import Any
from typing import ClassVar

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User


class BaseAdmin(admin.ModelAdmin):
    """Base admin class for all models."""

    ...


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """User admin class."""

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display: ClassVar = ["email", "name", "is_superuser"]
    search_fields: ClassVar = ["name"]
    ordering: ClassVar = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
