from django.contrib import admin

from .models import IntegrationConnection


@admin.register(IntegrationConnection)
class IntegrationConnectionAdmin(admin.ModelAdmin):
    list_display = ["client", "provider", "status", "last_sync_at"]
    list_filter = ["provider", "status"]
