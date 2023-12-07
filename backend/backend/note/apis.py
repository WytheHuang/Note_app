from uuid import UUID

from typing import Any
from django.contrib.auth.models import AnonymousUser

from core import schemas as core_schemas
from core import exceptions as core_exceptions
from core.apis import BaseEditApiController
from django.core.handlers.asgi import ASGIRequest
from ninja_extra import api_controller
from ninja_extra import route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import AsyncJWTAuth as JWTAuth

from asgiref.sync import sync_to_async

from . import models
from . import schemas


@api_controller(
    "/notebooks",
    auth=JWTAuth(),
    tags=["note_books"],
    permissions=[IsAuthenticated],
)
class NoteBookController(BaseEditApiController):
    Model = models.NoteBookModel

    @route.post(
        "",
        response={
            200: schemas.PostNoteBookResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
        },
    )
    async def create(self, request: ASGIRequest, body: schemas.PostNoteBookRequestSchema) -> schemas.PutNoteBookResponseSchema:
        """Create note book."""

        return await sync_to_async(super().create)(request=request, body=body)

    @route.get(
        "",
        response={
            200: list[schemas.GetNoteBookResponseSchema],
            401: core_schemas.Http401UnauthorizedSchema,
        },
    )
    async def get_all(self, request: ASGIRequest) -> list[schemas.GetNoteBookResponseSchema]:
        """Get all note books."""
        return await sync_to_async(super().get_all)(request=request)

    @route.get(
        "/{pk}",
        response={
            200: schemas.GetNoteBookResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def get(self, request: ASGIRequest, pk: UUID) -> schemas.GetNoteBookResponseSchema:
        """Get all note in note book."""
        return await sync_to_async(super().get)(request=request, pk=pk)

    @route.put(
        "/{pk}",
        response={
            200: schemas.PutNoteBookResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def update(self, request: ASGIRequest, pk: UUID, body: schemas.PutNoteBookRequestSchema) -> schemas.PutNoteBookResponseSchema:
        """Update note book."""
        return await sync_to_async(super().update)(request=request, pk=pk, body=body)

    @route.delete(
        "/{pk}",
        response={
            200: core_schemas.BaseResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def delete(self, request: ASGIRequest, pk: UUID) -> dict[Any, Any]:
        """Delete note book."""
        return await sync_to_async(super().delete)(request=request, pk=pk)
