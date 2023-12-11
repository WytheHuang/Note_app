from typing import Any
from uuid import UUID

from asgiref.sync import sync_to_async
from core import schemas as core_schemas
from core.exceptions import Http401UnauthorizedException
from core.exceptions import Http404NotFoundException
from core.apis import BaseEditApiController
from django.core.handlers.asgi import ASGIRequest
from django.contrib.auth.models import AnonymousUser

from ninja import Query
from ninja_extra import api_controller
from ninja_extra import route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import AsyncJWTAuth

from . import models
from . import schemas


@api_controller(
    "/notebooks",
    auth=AsyncJWTAuth(),
    tags=["note_books"],
    permissions=[IsAuthenticated],
)
class NoteBookController(BaseEditApiController):
    """NoteBook api controller."""

    Model = models.NoteBookModel

    @route.post(
        "",
        response={
            200: schemas.PostNoteBookResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
        },
    )
    async def create(self, request: ASGIRequest, body: schemas.PostNoteBookRequestSchema) -> schemas.PostNoteBookResponseSchema:
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


@api_controller(
    "/notes",
    auth=AsyncJWTAuth(),
    tags=["notes"],
    permissions=[IsAuthenticated],
)
class NoteController(BaseEditApiController):
    """Note api controller."""

    Model = models.NoteModel

    @route.post(
        "",
        response={
            200: schemas.PostNoteResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
        },
    )
    async def create(self, request: ASGIRequest, body: schemas.PostNoteRequestSchema) -> schemas.PostNoteResponseSchema:
        """Create note."""

        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        request_body = body.dict()
        note_book_id = request_body.pop("note_book")

        model = self.Model(  # type: ignore
            **request_body,
            note_book_id=note_book_id,
        )

        await sync_to_async(model.create)(request.user)

        return model

    @route.get(
        "",
        response={
            200: list[schemas.GetNoteResponseSchema],
            401: core_schemas.Http401UnauthorizedSchema,
        },
    )
    async def get_all(self, request: ASGIRequest, filter: Query[schemas.GetNoteFilterSchema]) -> list[schemas.GetNoteResponseSchema]:
        """Get all notes."""
        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        if filter.all:
            filter_dict = {}
        elif filter.is_archived or filter.is_trash:
            filter_dict = {
                "is_archived": filter.is_archived,
                "is_trash": filter.is_trash,
            }
        else:
            filter_dict = {
                "note_book_id": filter.note_book_id,
            }

        model = await sync_to_async(self.Model.objects.filter)(  # type: ignore
            created_by_user_id=request.user.id,  # type: ignore
            **filter_dict,  # type: ignore
        )

        response = await sync_to_async(model.values)()

        return await sync_to_async(list)(response)

    @route.get(
        "/{pk}",
        response={
            200: schemas.GetNoteResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def get(self, request: ASGIRequest, pk: UUID) -> schemas.GetNoteResponseSchema:
        """Get note."""
        return await sync_to_async(super().get)(request=request, pk=pk)

    @route.put(
        "/{pk}",
        response={
            200: schemas.PutNoteResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def update(self, request: ASGIRequest, pk: UUID, body: schemas.PutNoteRequestSchema) -> schemas.PutNoteResponseSchema:
        """Update note."""
        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        request_body = body.dict()
        note_book_id = request_body.pop("note_book")

        try:
            model = await sync_to_async(self.Model.objects.get)(  # type: ignore
                id=pk,
            )
        except self.Model.DoesNotExist as err:  # type: ignore
            raise Http404NotFoundException from err

        for k, v in request_body.items():
            setattr(model, k, v)

        model.note_book_id = note_book_id
        await sync_to_async(model.save)(request.user)

        return model

    @route.delete(
        "/{pk}",
        response={
            200: core_schemas.BaseResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def delete(self, request: ASGIRequest, pk: UUID) -> dict[Any, Any]:
        """Delete note."""
        return await sync_to_async(super().delete)(request=request, pk=pk)

    @route.patch(
        "/{pk}",
        response={
            200: schemas.PutNoteResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def patch(self, request: ASGIRequest, pk: UUID, body: schemas.PatchNoteRequestSchema) -> schemas.PutNoteResponseSchema:
        """Update note."""
        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        request_body = body.dict()
        request_body["note_book_id"] = request_body.pop("note_book")

        try:
            model = await sync_to_async(self.Model.objects.get)(  # type: ignore
                id=pk,
            )
        except self.Model.DoesNotExist as err:  # type: ignore
            raise Http404NotFoundException

        for k, v in request_body.items():
            if v is not None and getattr(model, k) != v:
                setattr(model, k, v)

        await sync_to_async(model.save)(request.user)

        return model

    @route.patch(
        "/set_note_book_none/{pk}",
        response={
            200: schemas.PutNoteResponseSchema,
            401: core_schemas.Http401UnauthorizedSchema,
            404: core_schemas.Http404NotFoundSchema,
        },
    )
    async def set_note_book_none(self, request: ASGIRequest, pk: UUID) -> schemas.PutNoteResponseSchema:
        """Update note."""
        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        try:
            model = await sync_to_async(self.Model.objects.get)(  # type: ignore
                id=pk,
            )
        except self.Model.DoesNotExist as err:  # type: ignore
            raise Http404NotFoundException

        model.note_book_id = None

        await sync_to_async(model.save)(request.user)

        return model
