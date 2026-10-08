from django.contrib import admin

from .models import Office


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ["trade_name", "legal_name", "tax_id", "is_active"]
    search_fields = ["trade_name", "legal_name", "tax_id"]
