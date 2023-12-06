from __future__ import annotations

from typing import Any
from uuid import UUID

from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import ModelBase
from ninja.orm.metaclass import ModelSchemaMetaclass
from ninja.schema import ResolverMetaclass
from ninja_extra import api_controller
from ninja_extra import route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from core.exceptions import Http401UnauthorizedException
from core.exceptions import Http404NotFoundException


class BaseEditApiController:
    """Base class for edit api controller. Every edit api controller should inherit from this class.

    Attributes:
        Model (ModelBase | None): django model class. must be set in child class.

        CreateModelRequestSchema (ModelSchemaMetaclass | ResolverMetaclass | None): create request schema. just for type hint.
        PutModelRequestSchema (ModelSchemaMetaclass | ResolverMetaclass | None): put request schema. just for type hint.
        GetModelResponseSchema (ModelSchemaMetaclass | ResolverMetaclass | None): get response schema. just for type hint.

        pk_field (str): django model primary key field name. default is "id". must be set in child class.

    Methods:
        create: base create method. for use just call super().create(request, body).
        get_all: base get all method. for use just call super().get_all(request).
        get: base get method. for use just call super().get(request, pk).
        update: base update method. for use just call super().update(request, pk, body).
        delete: base delete method. for use just call super().delete(request, pk).
    """

    Model: ModelBase | None = None

    CreateModelRequestSchema: ModelSchemaMetaclass | ResolverMetaclass | None = None
    PutModelRequestSchema: ModelSchemaMetaclass | ResolverMetaclass | None = None
    GetModelResponseSchema: ModelSchemaMetaclass | ResolverMetaclass | None = None

    def create(self, request: WSGIRequest, body: CreateModelRequestSchema) -> dict[str, Any]:  # type: ignore
        """Create object.

        Args:
            request (WSGIRequest): HTTP request.
            body (CreateModelRequestSchema): Request body. must be a pydantic model.

        Returns:
            dict[str, Any]: response body. must be json serializable. typically {"msg": "success"}.
        """
        company_id = request.user.company_id  # type: ignore

        q = self.Model(  # type: ignore
            **body.dict(),
            company_id=company_id,
        )

        q.create(request.user)

        return q

    def get_all(self, request: WSGIRequest) -> list[GetModelResponseSchema]:  # type: ignore
        """Get all objects belong to the user's company.

        Args:
            request (WSGIRequest): HTTP request.

        Returns:
            list[GetModelResponseSchema]: list of objects. must be json serializable.
        """
        company_id = request.user.company_id  # type: ignore

        q = self.Model.objects.filter(company_id=company_id).values()  # type: ignore

        return list(q)

    def get(self, request: WSGIRequest, pk: UUID) -> GetModelResponseSchema:  # type: ignore
        """Get object by primary key.

        Args:
            request (WSGIRequest): HTTP request.
            pk (int): primary key value of the object.

        Raises:
            Http404NotFoundException: if object not found.

        Returns:
            GetModelResponseSchema: object. must be json serializable.
        """
        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        try:
            q = self.Model.objects.get(  # type: ignore
                id=pk,
            )
        except self.Model.DoesNotExist as err:  # type: ignore
            raise Http404NotFoundException from err

        return q

    def update(self, request: WSGIRequest, pk: UUID, body: PutModelRequestSchema) -> dict[str, Any]:  # type: ignore
        """Update object by primary key.

        Args:
            request (WSGIRequest): HTTP request.
            pk (int): primary key value of the object.
            body (PutModelRequestSchema): new values of the object.

        Raises:
            Http401UnauthorizedException: if user is not authenticated.
            Http404NotFoundException: if object not found.

        Returns:
            dict[str, Any]: response body. must be json serializable. typically {"msg": "success"}.
        """
        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        try:
            model = self.Model.objects.select_for_update().get(  # type: ignore
                id=pk,
            )
        except self.Model.DoesNotExist as err:  # type: ignore
            raise Http404NotFoundException from err

        for k, v in body.dict().items():
            setattr(model, k, v)

        model.save(request.user)

        return {"msg": "success"}

    def delete(self, request: WSGIRequest, pk: UUID) -> dict[str, Any]:
        """Delete object by primary key.

        Args:
            request (WSGIRequest): HTTP request.
            pk (int): primary key value of the object.

        Raises:
            Http401UnauthorizedException: if user is not authenticated.
            Http404NotFoundException: if object not found.

        Returns:
            dict[str, Any]: response body. must be json serializable. typically {"msg": "success"}.
        """
        if isinstance(request.user, AnonymousUser):
            raise Http401UnauthorizedException

        try:
            q = self.Model.objects.get(  # type: ignore
                id=pk,
            )
        except self.Model.DoesNotExist as err:  # type: ignore
            raise Http404NotFoundException from err

        q.delete(request.user)

        return {"msg": "success"}


@api_controller(permissions=[IsAuthenticated], auth=JWTAuth(), prefix_or_class="core/")
class CoreController:
    """api controller for example."""

    @route.get("/example/")
    def example_api(self, request: WSGIRequest) -> dict[str, str]:
        """Example api.

        Args:
            request (WSGIRequest): http request.

        Returns:
            dict: a dict with some info. must be json serializable for response.
        """
        user_id = getattr(request.user, "id", None)
        company_id = getattr(request.user, "company_id", None)
        return {
            "u_id_type": str(type(user_id)),
            "c_id": str(company_id),
        }
