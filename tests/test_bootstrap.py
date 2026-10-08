import pytest
from django.core.management import call_command

from apps.accounts.models import User
from apps.offices.models import Office


@pytest.mark.django_db
def test_bootstrap_office_creates_office_and_admin(monkeypatch):
    monkeypatch.setenv("DJANGO_BOOTSTRAP_PASSWORD", "strong-test-password")

    call_command(
        "bootstrap_office",
        legal_name="Escritório Inicial Ltda",
        trade_name="Escritório Inicial",
        tax_id="12.345.678/0001-95",
        office_email="office@example.com",
        admin_email="owner@example.com",
        admin_name="Proprietário",
    )

    office = Office.objects.get()
    admin = User.objects.get()
    assert office.tax_id == "12345678000195"
    assert admin.office == office
    assert admin.is_superuser is True
    assert admin.check_password("strong-test-password")
