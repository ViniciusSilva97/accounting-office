from django.core.exceptions import ValidationError
from django.db import models


class AuditEvent(models.Model):
    office = models.ForeignKey(
        "offices.Office", on_delete=models.PROTECT, related_name="audit_events"
    )
    actor = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="audit_events",
        null=True,
        blank=True,
    )
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="audit_events",
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100)
    object_public_id = models.CharField(max_length=64)
    metadata = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-occurred_at", "-id"]
        indexes = [models.Index(fields=["office", "action", "occurred_at"])]

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Eventos de auditoria não podem ser alterados.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Eventos de auditoria não podem ser excluídos.")

    def __str__(self):
        return f"{self.action} — {self.object_type}:{self.object_public_id}"
