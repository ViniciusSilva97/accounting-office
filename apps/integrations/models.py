from django.db import models

from apps.core.models import PublicModel


class IntegrationConnection(PublicModel):
    class Provider(models.TextChoices):
        BLING = "BLING", "Bling"
        QUESTOR = "QUESTOR", "Questor"
        DOMINIO = "DOMINIO", "Domínio"
        FORTES = "FORTES", "Fortes"
        SCI = "SCI", "SCI"
        ALTERDATA = "ALTERDATA", "Alterdata"
        CONTMATIC = "CONTMATIC", "Contmatic"
        CALIMA = "CALIMA", "Calima"
        OTHER = "OTHER", "Outro"

    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Planejada"
        AUTHORIZATION_PENDING = "AUTHORIZATION_PENDING", "Aguardando autorização"
        CONNECTED = "CONNECTED", "Conectada"
        ERROR = "ERROR", "Com erro"
        DISABLED = "DISABLED", "Desativada"

    client = models.ForeignKey(
        "clients.Client", on_delete=models.PROTECT, related_name="integrations"
    )
    provider = models.CharField(max_length=30, choices=Provider.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PLANNED)
    external_account_id = models.CharField(max_length=180, blank=True)
    connected_at = models.DateTimeField(null=True, blank=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    non_secret_settings = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["client", "provider"], name="uniq_provider_per_client")
        ]

    def __str__(self):
        return f"{self.client} — {self.get_provider_display()}"
