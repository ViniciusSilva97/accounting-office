import pytest

from apps.accounts.models import User
from apps.clients.permissions import can_access_client
from apps.clients.services import register_client
from apps.offices.models import Office


@pytest.mark.django_db
def test_user_cannot_access_client_from_another_office(admin, client_data):
    client = register_client(actor=admin, data=client_data)
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
        role=User.Role.ADMIN,
    )

    assert can_access_client(outsider, client) is False
