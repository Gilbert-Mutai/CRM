from django.db import models
from django.conf import settings
from core.models import Client


class Domain(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="domains")
    domain = models.CharField(max_length=255, unique=True)

    HOST_CHOICES = [
        ("None", "None"),
        ("webhosting.angani", "webhosting.angani"),
        ("host-02.angani", "host-02.angani"),
        ("webhosting-03.angani", "webhosting-03.angani"),
    ]
    host = models.CharField(max_length=50, choices=HOST_CHOICES, default="None")

    package = models.IntegerField(blank=True, null=True)

    STATUS_CHOICES = [
        ("active", "Active"),
        ("expired", "Expired"),
        ("pending", "Pending"),
        ("suspended", "Suspended"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # Metadata fields
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="domain_created_by",
    )
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="domain_updated_by",
    )

    def __str__(self):
        return f"{self.client} - {self.domain} ({self.get_status_display()})"
