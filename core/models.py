from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings 
from django.core.validators import RegexValidator

class Client(models.Model):
    INDIVIDUAL = 'individual'
    COMPANY = 'company'
    CLIENT_TYPE_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (COMPANY, 'Company'),
    ]

    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, default=COMPANY)
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )

    # Audit trail
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='clients_created'
    )
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='clients_updated'
    )

    def clean(self):
        super().clean()
        if self.client_type == self.COMPANY and not self.contact_person:
            raise ValidationError({
                'contact_person': 'Contact person is required for company clients.'
            })

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name', 'email'], name='unique_client_name_email')
        ]
