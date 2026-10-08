from django.contrib import admin

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ["occurred_at", "office", "actor", "action", "object_type"]
    list_filter = ["office", "action"]
    search_fields = ["action", "object_type", "object_public_id"]
    readonly_fields = [
        "office",
        "actor",
        "client",
        "action",
        "object_type",
        "object_public_id",
        "metadata",
        "occurred_at",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
