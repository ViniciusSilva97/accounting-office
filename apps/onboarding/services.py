from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from apps.audit.services import record_event
from apps.clients.models import Client
from apps.clients.permissions import can_access_client

from .models import OnboardingTask

BASE_TASKS = (
    ("confirm_registration", "Confirmar dados cadastrais", 2),
    ("collect_authorizations", "Coletar procurações e autorizações", 3),
    ("map_obligations", "Mapear regime e obrigações", 5),
    ("configure_document_flow", "Configurar fluxo de documentos", 5),
    ("configure_operational_system", "Configurar ERP ou sistema operacional", 7),
    ("validate_opening_data", "Validar saldos e dados de abertura", 10),
)


def create_default_onboarding_tasks(*, client, responsible):
    today = timezone.localdate()
    tasks = [
        OnboardingTask(
            client=client,
            code=code,
            title=title,
            due_date=today + timedelta(days=days),
            assigned_to=responsible,
        )
        for code, title, days in BASE_TASKS
    ]
    return OnboardingTask.objects.bulk_create(tasks)


@transaction.atomic
def complete_onboarding_task(*, actor, task):
    if not can_access_client(actor, task.client):
        raise PermissionDenied("Você não pode alterar esta implantação.")
    if actor.role == actor.Role.VIEWER:
        raise PermissionDenied("Usuários de consulta não podem concluir tarefas.")
    if task.status == OnboardingTask.Status.DONE:
        return task

    task.status = OnboardingTask.Status.DONE
    task.completed_at = timezone.now()
    task.save(update_fields=["status", "completed_at", "updated_at"])
    record_event(
        office=task.client.office,
        actor=actor,
        client=task.client,
        action="onboarding.task_completed",
        instance=task,
        metadata={"code": task.code},
    )

    required_open = task.client.onboarding_tasks.filter(is_required=True).exclude(
        status=OnboardingTask.Status.DONE
    )
    if not required_open.exists() and task.client.status == Client.Status.ONBOARDING:
        task.client.status = Client.Status.ACTIVE
        task.client.save(update_fields=["status", "updated_at"])
        record_event(
            office=task.client.office,
            actor=actor,
            client=task.client,
            action="client.activated",
            instance=task.client,
        )
    return task
