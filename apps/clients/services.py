from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from apps.audit.services import record_event
from apps.core.documents import normalize_tax_id
from apps.onboarding.services import create_default_onboarding_tasks

from .models import Client, ClientAssignment
from .permissions import can_register_client


@transaction.atomic
def register_client(*, actor, data, responsible=None):
    if not can_register_client(actor) or actor.office_id is None:
        raise PermissionDenied("Você não pode cadastrar clientes.")

    tax_id = normalize_tax_id(data["tax_id"])
    expected_length = 14 if data["entity_type"] == Client.EntityType.COMPANY else 11
    if len(tax_id) != expected_length:
        raise ValidationError("O documento não corresponde ao tipo de pessoa selecionado.")

    client = Client.objects.create(
        office=actor.office,
        entity_type=data["entity_type"],
        tax_id=tax_id,
        legal_name=data["legal_name"].strip(),
        trade_name=data.get("trade_name", "").strip(),
        service_scope=data["service_scope"],
        email=data.get("email", "").strip(),
        phone=data.get("phone", "").strip(),
        start_of_service=data["start_of_service"],
    )

    responsible = responsible or actor
    if responsible.office_id != actor.office_id:
        raise ValidationError("O responsável deve pertencer ao mesmo escritório.")
    ClientAssignment.objects.create(
        client=client,
        user=responsible,
        access_level=ClientAssignment.AccessLevel.RESPONSIBLE,
        assigned_by=actor,
    )
    tasks = create_default_onboarding_tasks(client=client, responsible=responsible)
    record_event(
        office=actor.office,
        actor=actor,
        client=client,
        action="client.registered",
        instance=client,
        metadata={"onboarding_tasks_created": len(tasks)},
    )
    return client
