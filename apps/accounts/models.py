import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        ACCOUNTANT = "ACCOUNTANT", "Contador"
        ANALYST = "ANALYST", "Analista"
        VIEWER = "VIEWER", "Consulta"

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    office = models.ForeignKey(
        "offices.Office", on_delete=models.PROTECT, related_name="users", null=True, blank=True
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=180)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ANALYST)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        ordering = ["full_name", "email"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(is_superuser=True) | models.Q(office__isnull=False),
                name="regular_user_requires_office",
            )
        ]

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.email
