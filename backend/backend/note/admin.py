from core.admin import BaseAdmin
from django.contrib import admin

from . import models


@admin.register(models.NoteModel)
class NoteModelAdmin(BaseAdmin):
    """Note model admin."""


@admin.register(models.NoteBookModel)
class NoteBookModelAdmin(BaseAdmin):
    """Note book model admin."""
