from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db.models import Manager
from django.db.models.query import QuerySet


class UserManager(DjangoUserManager, Manager):
    """Custom user manager for the User model."""

    def _create_user(self, email: str, password: str | None, **extra_fields: dict):  # noqa: ANN202
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: dict):
        """Create user public Manager method.

        Args:
            email (str): email of the user.
            password (str | None, optional): user password. Defaults to None.
            **extra_fields (dict): extra fields for creating user.

        Returns:
            User: User object just created.
        """
        extra_fields.setdefault("is_staff", False)  # type: ignore
        extra_fields.setdefault("is_superuser", False)  # type: ignore
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: dict):
        """Create superuser public Manager method.

        Args:
            email (str): email of the user.
            password (str | None, optional): user password. Defaults to None.
            **extra_fields (dict): extra fields for creating user.

        Raises:
            ValueError: is_staff and is_superuser must be True.

        Returns:
            User: User object just created.
        """
        extra_fields.setdefault("is_staff", True)  # type: ignore
        extra_fields.setdefault("is_superuser", True)  # type: ignore

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_queryset(self) -> QuerySet:
        """Overwritten get_queryset method for soft delete.

        Returns:
            QuerySet: QuerySet object.
        """
        return super().get_queryset().exclude(is_delete=True)


class BaseModelManager(Manager):
    """Base model manager for all models."""

    def get_queryset(self) -> QuerySet:
        """Overwritten get_queryset method for soft delete.

        Returns:
            QuerySet: QuerySet object.
        """
        return super().get_queryset().exclude(is_delete=True)
