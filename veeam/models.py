from django.db import models
from django.conf import settings
from django.db.models import Q
from core.models import Client


class VeeamJob(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="veeam_created_records",
        verbose_name="Created By",
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="veeam_records",
        verbose_name="Client",
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

    site = models.CharField(max_length=50, choices=SITE_CHOICES, verbose_name="Site")
    computer_name = models.CharField(max_length=100, verbose_name="Computer Name")
    tag = models.CharField(
        max_length=100, default="Not set", blank=True, verbose_name="Tag"
    )
    os = models.CharField(
        max_length=20, choices=OS_CHOICES, verbose_name="Operating System"
    )
    managed_by = models.CharField(
        max_length=20, choices=MANAGED_BY_CHOICES, verbose_name="Managed By"
    )
    job_status = models.CharField(
        max_length=20,
        choices=JOB_STATUS_CHOICES,
        default="Running",
        verbose_name="Job Status",
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Comment")

    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="veeam_updated_records",
        verbose_name="Updated By",
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
        constraints = [
            models.UniqueConstraint(
                name="unique_client_computer_ci", fields=["client", "computer_name"]
            )
        ]
        ordering = ["-last_updated"]
        verbose_name = "Veeam Job"
        verbose_name_plural = "Veeam Jobs"
