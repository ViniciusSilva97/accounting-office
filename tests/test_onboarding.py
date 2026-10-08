import pytest
from django.core.exceptions import PermissionDenied

from apps.accounts.models import User
from apps.audit.models import AuditEvent
from apps.clients.models import ClientAssignment
from apps.clients.services import register_client
from apps.onboarding.models import OnboardingTask
from apps.onboarding.services import complete_onboarding_task


@pytest.mark.django_db
def test_last_required_task_activates_client(admin, client_data):
    client = register_client(actor=admin, data=client_data)

    for task in client.onboarding_tasks.all():
        complete_onboarding_task(actor=admin, task=task)

    client.refresh_from_db()
    assert client.status == client.Status.ACTIVE
    assert AuditEvent.objects.filter(client=client, action="client.activated").count() == 1


@pytest.mark.django_db
def test_complete_task_is_idempotent(admin, client_data):
    client = register_client(actor=admin, data=client_data)
    task = client.onboarding_tasks.first()

    complete_onboarding_task(actor=admin, task=task)
    complete_onboarding_task(actor=admin, task=task)

    assert AuditEvent.objects.filter(action="onboarding.task_completed", client=client).count() == 1


@pytest.mark.django_db
def test_viewer_cannot_complete_task(admin, client_data):
    client = register_client(actor=admin, data=client_data)
    viewer = User.objects.create_user(
        email="viewer@example.com",
        password="testing-password",
        full_name="Consulta",
        office=admin.office,
        role=User.Role.VIEWER,
    )
    ClientAssignment.objects.create(
        client=client,
        user=viewer,
        access_level=ClientAssignment.AccessLevel.VIEWER,
        assigned_by=admin,
    )

    with pytest.raises(PermissionDenied):
        complete_onboarding_task(actor=viewer, task=client.onboarding_tasks.first())

    assert client.onboarding_tasks.filter(status=OnboardingTask.Status.DONE).count() == 0
