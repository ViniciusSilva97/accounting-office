import pytest
from django.core.exceptions import ValidationError

from apps.audit.models import AuditEvent
from apps.clients.services import register_client


@pytest.mark.django_db
def test_audit_event_cannot_be_changed_or_deleted(admin, client_data):
    client = register_client(actor=admin, data=client_data)
    event = AuditEvent.objects.get(client=client, action="client.registered")
    event.action = "tampered"

    with pytest.raises(ValidationError):
        event.save()
    with pytest.raises(ValidationError):
        event.delete()
