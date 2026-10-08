import pytest
from django.urls import reverse

from apps.clients.services import register_client


@pytest.mark.django_db
def test_dashboard_requires_login(client):
    response = client.get(reverse("dashboard"))
    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_admin_sees_registered_client(client, admin, client_data):
    registered = register_client(actor=admin, data=client_data)
    client.force_login(admin)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    assert registered.trade_name.encode() in response.content


@pytest.mark.django_db
def test_task_completion_endpoint(client, admin, client_data):
    registered = register_client(actor=admin, data=client_data)
    task = registered.onboarding_tasks.first()
    client.force_login(admin)

    response = client.post(
        reverse("onboarding-task-complete", args=[registered.public_id, task.public_id])
    )

    assert response.status_code == 302
    task.refresh_from_db()
    assert task.status == task.Status.DONE


@pytest.mark.django_db
def test_admin_can_register_client_from_form(client, admin, client_data):
    client.force_login(admin)

    response = client.post(reverse("client-create"), data=client_data)

    assert response.status_code == 302
    assert response.url.startswith("/clientes/")
