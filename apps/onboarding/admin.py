from django.contrib import admin

from .models import OnboardingTask


@admin.register(OnboardingTask)
class OnboardingTaskAdmin(admin.ModelAdmin):
    list_display = ["title", "client", "assigned_to", "status", "due_date"]
    list_filter = ["status", "is_required"]
    search_fields = ["title", "client__legal_name", "client__trade_name"]
