from django.db import models
from django.conf import settings
from core.models import Client


class SDWAN(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sdwan_created_records",
        verbose_name="Created By",
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="sdwan_records",
        verbose_name="Client",
    )

    account_number = models.CharField(
        max_length=50,
        verbose_name="Account Number",
    )

    PROVIDER_CHOICES = [
        ("Safaricom", "Safaricom"),
        ("Liquid Telecom", "Liquid Telecom"),
        ("Telkom", "Telkom"),
        ("MTN", "MTN"),
        ("Other", "Other"),
    ]

    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES,
        verbose_name="Provider",
    )

    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sdwan_updated_records",
        verbose_name="Updated By",
    )

    def __str__(self):
        return f"{self.client.name} - {self.provider} ({self.account_number})"

    class Meta:
        indexes = [
            models.Index(fields=["account_number"]),
            models.Index(fields=["provider"]),
        ]
        constraints = [
            models.UniqueConstraint(
                name="unique_client_account_number",
                fields=["client", "account_number"],
            )
        ]
        ordering = ["-last_updated"]
        verbose_name = "SD-WAN"
        verbose_name_plural = "SD-WAN Records"
