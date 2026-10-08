from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("clientes/novo/", views.client_create, name="client-create"),
    path("clientes/<uuid:public_id>/", views.client_detail, name="client-detail"),
    path(
        "clientes/<uuid:public_id>/tarefas/<uuid:task_public_id>/concluir/",
        views.complete_task,
        name="onboarding-task-complete",
    ),
]
