from typing import ClassVar

from core.models import BaseModel
from django.db import models


# Create your models here.


class NoteBookModel(BaseModel):
    """Note book model.

    Attributes:
        title (str): note book title.
    """

    title = models.CharField(max_length=255)

    class Meta:
        """Meta class."""

        verbose_name: ClassVar = "Note Book"
        verbose_name_plural: ClassVar = "Note Books"
        ordering: ClassVar = ["-created_at"]
        indexes: ClassVar = [
            models.Index(fields=["id"]),
        ]

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: string representation.
        """
        return self.title


class NoteModel(BaseModel):
    """Note model.

    Attributes:
        title (str): note title.
        content (str): note content.
        is_archived (bool): is archived.
        is_pinned (bool): is pinned.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    is_archived = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)

    note_book = models.ForeignKey(NoteBookModel, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    class PermissionOptions(models.IntegerChoices):
        """Permission options."""

        DO_NOTHING = 0, "Do nothing"
        CAN_READ = 1, "Can read"
        CAN_EDIT = 2, "Can edit"

    other_user_permission = models.IntegerField(
        default=PermissionOptions.DO_NOTHING,
        choices=PermissionOptions.choices,
    )

    class Meta:
        """Meta class."""

        verbose_name: ClassVar = "Note"
        verbose_name_plural: ClassVar = "Notes"
        ordering: ClassVar = ["-created_at"]
        indexes: ClassVar = [
            models.Index(fields=["id"]),
        ]

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: string representation.
        """
        return self.title
