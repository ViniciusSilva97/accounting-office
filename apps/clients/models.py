from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.core.models import PublicModel


class Client(PublicModel):
    class EntityType(models.TextChoices):
        COMPANY = "COMPANY", "Pessoa jurídica"
        INDIVIDUAL = "INDIVIDUAL", "Pessoa física"

    class Status(models.TextChoices):
        ONBOARDING = "ONBOARDING", "Em implantação"
        ACTIVE = "ACTIVE", "Ativa"
        SUSPENDED = "SUSPENDED", "Suspensa"
        CLOSED = "CLOSED", "Encerrada"

    class ServiceScope(models.TextChoices):
        SERVICES = "SERVICES", "Prestação de serviços"
        COMMERCE = "COMMERCE", "Comércio"
        MIXED = "MIXED", "Mista"

    office = models.ForeignKey("offices.Office", on_delete=models.PROTECT, related_name="clients")
    entity_type = models.CharField(max_length=20, choices=EntityType.choices)
    tax_id = models.CharField(max_length=14)
    legal_name = models.CharField(max_length=255)
    trade_name = models.CharField(max_length=255, blank=True)
    service_scope = models.CharField(max_length=20, choices=ServiceScope.choices)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    start_of_service = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ONBOARDING)

    class Meta:
        ordering = ["trade_name", "legal_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["office", "entity_type", "tax_id"], name="uniq_client_tax_id_per_office"
            )
        ]

    def __str__(self):
        return self.trade_name or self.legal_name


class ClientAssignment(models.Model):
    class AccessLevel(models.TextChoices):
        RESPONSIBLE = "RESPONSIBLE", "Responsável"
        CONTRIBUTOR = "CONTRIBUTOR", "Colaborador"
        VIEWER = "VIEWER", "Consulta"

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="assignments")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="client_assignments"
    )
    access_level = models.CharField(max_length=20, choices=AccessLevel.choices)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assignments_granted"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["client", "user"],
                condition=Q(revoked_at__isnull=True),
                name="uniq_active_client_assignment",
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.client}"
