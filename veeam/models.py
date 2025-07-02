from django.db import models
from django.conf import settings
from core.models import Client


class Veeam(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="veeam_created_records",
    )

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="veeam_records"
    )

    SITE_CHOICES = [
        ("Angani ADC", "Angani ADC"),
        ("Angani Icolo", "Angani Icolo"),
    ]

    OS_CHOICES = [
        ("Linux", "Linux"),
        ("Windows", "Windows"),
    ]

    MANAGED_BY_CHOICES = [
        ("Backup Agent", "Backup Agent"),
        ("VBR", "VBR"),
    ]

    JOB_STATUS_CHOICES = [
        ("Running", "Running"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]

    site = models.CharField(max_length=50, choices=SITE_CHOICES)
    computer_name = models.CharField(max_length=100)
    os = models.CharField(max_length=20, choices=OS_CHOICES)
    managed_by = models.CharField(max_length=20, choices=MANAGED_BY_CHOICES)
    job_status = models.CharField(
        max_length=20, choices=JOB_STATUS_CHOICES, default="Running"
    )
    comment = models.TextField(blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="veeam_updated_records",
    )

    def __str__(self):
        return f"{self.client.name} - {self.computer_name}"

    class Meta:
        indexes = [
            models.Index(fields=["computer_name"]),
            models.Index(fields=["site"]),
            models.Index(fields=["os"]),
            models.Index(fields=["managed_by"]),
            models.Index(fields=["job_status"]),
        ]
