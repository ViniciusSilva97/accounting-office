import pytest
from django.core.exceptions import PermissionDenied, ValidationError

from apps.accounts.models import User
from apps.audit.models import AuditEvent
from apps.clients.models import Client, ClientAssignment
from apps.clients.services import register_client
from apps.offices.models import Office
from apps.onboarding.services import BASE_TASKS


@pytest.mark.django_db
def test_register_client_creates_assignment_tasks_and_audit(admin, client_data):
    client = register_client(actor=admin, data=client_data)

    assert client.office == admin.office
    assert client.tax_id == "12345678000195"
    assert client.status == Client.Status.ONBOARDING
    assert client.onboarding_tasks.count() == len(BASE_TASKS)
    assert ClientAssignment.objects.filter(
        client=client, user=admin, revoked_at__isnull=True
    ).exists()
    assert AuditEvent.objects.filter(client=client, action="client.registered").exists()


@pytest.mark.django_db
def test_analyst_cannot_register_client(office, client_data):
    analyst = User.objects.create_user(
        email="analyst@example.com",
        password="testing-password",
        full_name="Analista",
        office=office,
        role=User.Role.ANALYST,
    )

    with pytest.raises(PermissionDenied):
        register_client(actor=analyst, data=client_data)

    assert Client.objects.count() == 0


@pytest.mark.django_db
def test_responsible_from_another_office_rolls_back_everything(admin, client_data):
    other_office = Office.objects.create(
        legal_name="Outro Escritório Ltda",
        tax_id="98765432000199",
        email="outro@example.com",
    )
    outsider = User.objects.create_user(
        email="outsider@example.com",
        password="testing-password",
        full_name="Usuário Externo",
        office=other_office,
        role=User.Role.ACCOUNTANT,
    )

    with pytest.raises(ValidationError):
        register_client(actor=admin, data=client_data, responsible=outsider)

    assert Client.objects.count() == 0
    assert AuditEvent.objects.count() == 0
