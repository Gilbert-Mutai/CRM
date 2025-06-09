from django.db import models
from django.utils import timezone
from django.conf import settings
from core.models import Client

class Project(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    ]

    CERTIFICATE_CHOICES = [
        ('Shared', 'Shared'),
        ('Pending', 'Pending'),
    ]

    date_of_request = models.DateTimeField(default=timezone.now)
    customer_name = models.ForeignKey(Client, on_delete=models.CASCADE)
    service_description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    date_of_completion = models.DateTimeField(null=True, blank=True)
    job_completion_certificate = models.CharField(max_length=10, choices=CERTIFICATE_CHOICES, default='Pending')
    engineer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'groups__name': 'Engineers'}
    )
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='projects_created'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='projects_updated'
    )

    def __str__(self):
        return f"Project: {self.customer_name.name} - {self.status}"

    class Meta:
        ordering = ['-date_of_request']
