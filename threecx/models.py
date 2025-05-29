from django.db import models
from django.conf import settings 

class ThreeCX(models.Model):
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='threecx_created_records'
    )

    # Business fields
    company_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    contact_details = models.CharField(max_length=50)

    # Dropdown choices
    SIP_PROVIDERS = [
        ('Angani', 'Angani'),
        ('Safaricom', 'Safaricom'),
        ('Airtel', 'Airtel'),
    ]
    sip_provider = models.CharField(max_length=20, choices=SIP_PROVIDERS)

    fqdn = models.CharField(max_length=100)

    LICENSE_TYPES = [
        ('3CX Standard', '3CX Standard'),
        ('3CX Pro', '3CX Pro'),
        ('3CX Enterprise', '3CX Enterprise'),
    ]
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPES)

    # Audit trail
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='threecx_updated_records'
    )

    def __str__(self):
        return self.company_name

    class Meta:
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['email_address']),
            models.Index(fields=['fqdn']),
            models.Index(fields=['sip_provider']),
            models.Index(fields=['license_type']),
        ]
