from django.contrib import admin
from .models import VeeamJob


@admin.register(VeeamJob)
class VeeamAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "site",
        "computer_name",
        "tag",
        "os",
        "managed_by",
        "job_status",
        "created_at",
        "last_updated",
    )
    list_filter = ("site", "os", "job_status")
    search_fields = ("client__name", "computer_name", "email")
    readonly_fields = ("created_at", "last_updated")
