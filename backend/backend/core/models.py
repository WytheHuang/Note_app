import uuid
from datetime import datetime
from typing import Any
from typing import ClassVar

import pytz
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import BaseModelManager
from .managers import UserManager


class User(AbstractUser):
    """Custom user model representing a user in the application.

    This custom user model extends the AbstractUser class and provides additional fields and behavior
    specific to the application's requirements.

    Attributes:
        id (UUIDField): The unique identifier for the user.
        company (ForeignKey to Company): The associated company for the user, if applicable.
        name (CharField): The name of the user.
        email (EmailField): The user's email address (used as the login identifier).
        updated_at (DateTimeField): The timestamp when the user record was last updated.
        is_delete (BooleanField): Indicates if the user record is marked as deleted.

    Fields:
        USERNAME_FIELD (str): The field used as the unique identifier for user login (set to "email").
        REQUIRED_FIELDS (list[str]): The list of fields required when creating a user (empty list).

    Methods:
        delete(self) -> None:
            Marks the user record as deleted by setting the 'is_delete' flag to True and deactivating the user.

    objects (UserManager): The manager for this user model.

    """

    id = models.UUIDField(
        verbose_name="userId",
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        auto_created=True,
    )
    name = models.CharField("Name of User", blank=True, max_length=255)
    first_name = None
    last_name = None
    email = models.EmailField("email address", unique=True)
    username = None

    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar = []

    objects = UserManager()

    def delete(self) -> None:
        """Marks the record as deleted. (Soft delete).

        This method sets the 'is_delete' flag to True, indicating that the record has been marked as deleted.
        The record is then saved to persist the deletion.

        Args:
            None

        Returns:
            None

        """
        self.is_delete = True
        self.is_active = False
        self.deleted_at = datetime.now(tz=pytz.timezone("Asia/Taipei"))
        self.save()


class BaseModel(models.Model):
    """Base model for all database models in the application.

    This abstract base model defines common fields and methods for other database models.
    It includes fields for tracking creation and modification timestamps, user associations,
    and soft deletion status. The model is tied to a company.

    Attributes:
        created_at (DateTimeField): The timestamp when the record was created.
        created_by_user (ForeignKey): The user who created the record.
        updated_at (DateTimeField): The timestamp when the record was last updated.
        updated_by_user (ForeignKey): The user who last updated the record.
        is_delete (BooleanField): Indicates if the record is marked as deleted.
        deleted_by_user (ForeignKey): The user who marked the record as deleted.
        company (ForeignKey): The associated company.

    Methods:
        save(self, user: AbstractBaseUser, *args: list[Any], **kwargs: dict[Any, Any]):
            Saves the model instance, updating the modified timestamp and associating the user who updated it.

        create(self, user: AbstractBaseUser, *args: list[Any], **kwargs: dict[Any, Any]):
            Creates and saves a new model instance, associating the user who created it.

        delete(self, user: AbstractBaseUser) -> None:
            Marks the model instance as deleted, associating the user who marked it as deleted.
    """

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    created_at = models.DateTimeField(default=timezone.now)
    created_by_user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_created_by_user",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by_user",
    )
    is_delete = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by_user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_deleted_by_user",
    )

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def save(self, user: AbstractBaseUser, *args: list[Any], **kwargs: dict[Any, Any]):
        """Save and update the object with user information.

        This method saves or updates the object and sets the 'updated_by_user' field to the specified user.
        Additionally, any extra keyword arguments provided will be applied to the object.

        Args:
            user (AbstractBaseUser): The user responsible for the update.
            *args (list[Any]): Additional positional arguments.
            **kwargs (dict[Any, Any]): Additional keyword arguments to be applied to the object.

        Returns:
            None

        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.updated_by_user = user
        super().save(*args, **kwargs)  # type: ignore

    def create(self, user: AbstractBaseUser, *args: list[Any], **kwargs: dict[Any, Any]):
        """Create a new object with user information.

        This method creates a new object and sets the 'created_by_user' and 'updated_by_user' fields to the specified user.
        Additionally, any extra keyword arguments provided will be applied to the object.

        Args:
            user (AbstractBaseUser): The user responsible for creating the object.
            *args (list[Any]): Additional positional arguments.
            **kwargs (dict[Any, Any]): Additional keyword arguments to be applied to the object.

        Returns:
            None

        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.created_by_user = user
        self.updated_by_user = user
        super().save(*args, **kwargs)  # type: ignore

    def delete(self, user: AbstractBaseUser) -> None:
        """Marks this object as deleted and assigns the user responsible for the deletion. (soft delete).

        The `delete` method sets the `is_delete` flag to True, indicating that the object is deleted,
        and records the `user` responsible for the deletion. After making these changes, it saves
        the object.

        Args:
            user (AbstractBaseUser): The user who is initiating the deletion.

        Returns:
            None: This method doesn't return a value.

        Note:
            The `save` method is called internally to persist the changes.
        """
        self.is_delete = True
        self.deleted_by_user = user
        self.deleted_at = datetime.now(tz=pytz.timezone("Asia/Taipei"))
        self.save(user)
