from typing import ClassVar

from core.utils import BASE_EXCLUDE_FIELD
from ninja import ModelSchema

from . import models


class PostNoteBookRequestSchema(ModelSchema):
    """Post note book request schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = BASE_EXCLUDE_FIELD


class PostNoteBookResponseSchema(ModelSchema):
    """Post note book response schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = BASE_EXCLUDE_FIELD


class PutNoteBookRequestSchema(ModelSchema):
    """Put note book request schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = BASE_EXCLUDE_FIELD


class PutNoteBookResponseSchema(ModelSchema):
    """Put note book response schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = BASE_EXCLUDE_FIELD


class GetNoteBookResponseSchema(ModelSchema):
    """Get note book response schema."""

    class Meta:
        model = models.NoteBookModel
        exclude: ClassVar = [
            "created_at",
            "created_by_user",
            "updated_at",
            "updated_by_user",
            "is_delete",
            "deleted_at",
            "deleted_by_user",
        ]


class CreateNoteRequestSchema(ModelSchema):
    """Create note request schema."""

    class Meta:
        model = models.NoteModel
        exclude = BASE_EXCLUDE_FIELD


class PutNoteRequestSchema(ModelSchema):
    """Put note request schema."""

    class Meta:
        model = models.NoteModel
        exclude = BASE_EXCLUDE_FIELD


class GetNoteResponseSchema(ModelSchema):
    """Get note response schema."""

    class Meta:
        model = models.NoteModel
        exclude = BASE_EXCLUDE_FIELD
