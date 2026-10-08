from django.db import models

from apps.core.models import PublicModel


class Office(PublicModel):
    legal_name = models.CharField(max_length=255)
    trade_name = models.CharField(max_length=255, blank=True)
    tax_id = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    timezone = models.CharField(max_length=64, default="America/Sao_Paulo")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["trade_name", "legal_name"]

    def __str__(self):
        return self.trade_name or self.legal_name
