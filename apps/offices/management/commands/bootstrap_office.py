import getpass
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.accounts.models import User
from apps.core.documents import normalize_tax_id
from apps.offices.models import Office


class Command(BaseCommand):
    help = "Cria o primeiro escritório e seu administrador."

    def add_arguments(self, parser):
        parser.add_argument("--legal-name", required=True)
        parser.add_argument("--trade-name", default="")
        parser.add_argument("--tax-id", required=True)
        parser.add_argument("--office-email", required=True)
        parser.add_argument("--admin-email", required=True)
        parser.add_argument("--admin-name", required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        if Office.objects.exists() or User.objects.exists():
            raise CommandError("A configuração inicial já foi executada.")

        password = os.getenv("DJANGO_BOOTSTRAP_PASSWORD") or getpass.getpass(
            "Senha do administrador: "
        )
        if len(password) < 12:
            raise CommandError("A senha deve ter pelo menos 12 caracteres.")

        office = Office.objects.create(
            legal_name=options["legal_name"].strip(),
            trade_name=options["trade_name"].strip(),
            tax_id=normalize_tax_id(options["tax_id"]),
            email=options["office_email"].strip().lower(),
        )
        User.objects.create_superuser(
            email=options["admin_email"],
            password=password,
            full_name=options["admin_name"].strip(),
            office=office,
        )
        self.stdout.write(self.style.SUCCESS("Escritório e administrador criados."))
