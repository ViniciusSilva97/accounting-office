from django.conf import settings
from django.db import models

from apps.core.models import PublicModel


class OnboardingTask(PublicModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        IN_PROGRESS = "IN_PROGRESS", "Em andamento"
        DONE = "DONE", "Concluída"
        BLOCKED = "BLOCKED", "Bloqueada"

    client = models.ForeignKey(
        "clients.Client", on_delete=models.PROTECT, related_name="onboarding_tasks"
    )
    code = models.CharField(max_length=60)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    is_required = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="onboarding_tasks",
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["client", "code"], name="uniq_onboarding_code_per_client"
            )
        ]

    def __str__(self):
        return f"{self.client}: {self.title}"
