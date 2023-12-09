from typing import ClassVar
from uuid import UUID

from core.utils import BASE_EXCLUDE_FIELD
from ninja import ModelSchema
from ninja import Schema

from . import models


class PostNoteBookRequestSchema(ModelSchema):
    """Post note book request schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = ["id"] + BASE_EXCLUDE_FIELD


class PostNoteBookResponseSchema(ModelSchema):
    """Post note book response schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = BASE_EXCLUDE_FIELD


class PutNoteBookRequestSchema(ModelSchema):
    """Put note book request schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = ["id"] + BASE_EXCLUDE_FIELD


class PutNoteBookResponseSchema(ModelSchema):
    """Put note book response schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = BASE_EXCLUDE_FIELD


class GetNoteBookResponseSchema(ModelSchema):
    """Get note book response schema."""

    class Meta:
        model = models.NoteBookModel
        exclude = BASE_EXCLUDE_FIELD


class PostNoteRequestSchema(ModelSchema):
    """Post note request schema."""

    class Meta:
        model = models.NoteModel
        exclude = ["id"] + BASE_EXCLUDE_FIELD


class PostNoteResponseSchema(ModelSchema):
    """Post note response schema."""

    class Meta:
        model = models.NoteModel
        exclude = BASE_EXCLUDE_FIELD


class PutNoteRequestSchema(ModelSchema):
    """Put note request schema."""

    class Meta:
        model = models.NoteModel
        exclude = ["id"] + BASE_EXCLUDE_FIELD


class PutNoteResponseSchema(ModelSchema):
    """Put note response schema."""

    class Meta:
        model = models.NoteModel
        exclude = BASE_EXCLUDE_FIELD


class GetNoteFilterSchema(Schema):
    """Get note request schema."""

    all: bool = True

    note_book_id: UUID = None  # type: ignore
    is_archived: bool = False
    is_trash: bool = False

    class Meta:
        fields_optional = ["note_book_id", "is_archived", "is_trash"]


class GetNoteResponseSchema(ModelSchema):
    """Get note response schema."""

    class Meta:
        model = models.NoteModel
        exclude = BASE_EXCLUDE_FIELD


class PatchNoteRequestSchema(ModelSchema):
    """Patch note request schema."""

    class Meta:
        model = models.NoteModel
        exclude = ["id"] + BASE_EXCLUDE_FIELD
        fields_optional = ["title", "content", "is_archived", "is_trash", "is_pinned"]


class GetNoteByNoteBookRequestSchema(Schema):
    """Get note by note book request schema."""

    note_book_id: UUID
