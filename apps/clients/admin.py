from django.contrib import admin

from .models import Client, ClientAssignment


class ClientAssignmentInline(admin.TabularInline):
    model = ClientAssignment
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["trade_name", "legal_name", "office", "service_scope", "status"]
    list_filter = ["office", "service_scope", "status"]
    search_fields = ["trade_name", "legal_name", "tax_id"]
    inlines = [ClientAssignmentInline]
