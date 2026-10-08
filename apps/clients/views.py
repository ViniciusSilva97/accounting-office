from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from apps.onboarding.models import OnboardingTask
from apps.onboarding.services import complete_onboarding_task

from .forms import ClientRegistrationForm
from .models import Client
from .permissions import can_access_client, can_register_client
from .services import register_client


def _accessible_clients(user):
    queryset = Client.objects.filter(office=user.office)
    if user.role != user.Role.ADMIN:
        queryset = queryset.filter(assignments__user=user, assignments__revoked_at__isnull=True)
    return queryset.distinct()


@login_required
def dashboard(request):
    clients = _accessible_clients(request.user)
    return render(request, "clients/dashboard.html", {"clients": clients})


@login_required
def client_create(request):
    if not can_register_client(request.user):
        raise PermissionDenied
    form = ClientRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            client = register_client(actor=request.user, data=form.cleaned_data)
        except (ValidationError, IntegrityError) as exc:
            form.add_error(None, str(exc))
        else:
            messages.success(request, "Cliente cadastrado e checklist criado.")
            return redirect("client-detail", public_id=client.public_id)
    return render(request, "clients/client_form.html", {"form": form})


@login_required
def client_detail(request, public_id):
    client = get_object_or_404(
        Client.objects.prefetch_related("onboarding_tasks"), public_id=public_id
    )
    if not can_access_client(request.user, client):
        raise PermissionDenied
    return render(request, "clients/client_detail.html", {"client": client})


@login_required
def complete_task(request, public_id, task_public_id):
    if request.method != "POST":
        raise PermissionDenied
    client = get_object_or_404(Client, public_id=public_id)
    task = get_object_or_404(OnboardingTask, public_id=task_public_id, client=client)
    complete_onboarding_task(actor=request.user, task=task)
    messages.success(request, "Tarefa concluída.")
    return redirect("client-detail", public_id=client.public_id)
