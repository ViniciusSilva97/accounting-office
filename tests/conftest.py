from datetime import date

import pytest

from apps.accounts.models import User
from apps.offices.models import Office


@pytest.fixture
def office(db):
    return Office.objects.create(
        legal_name="Escritório Teste Ltda",
        trade_name="Escritório Teste",
        tax_id="12345678000199",
        email="contato@example.com",
    )


@pytest.fixture
def admin(office):
    return User.objects.create_user(
        email="admin@example.com",
        password="testing-password",
        full_name="Administrador",
        office=office,
        role=User.Role.ADMIN,
    )


@pytest.fixture
def client_data():
    return {
        "entity_type": "COMPANY",
        "tax_id": "12.345.678/0001-95",
        "legal_name": "Cliente Exemplo Ltda",
        "trade_name": "Cliente Exemplo",
        "service_scope": "SERVICES",
        "email": "cliente@example.com",
        "phone": "31999999999",
        "start_of_service": date(2026, 10, 1),
    }
