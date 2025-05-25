from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name
    

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

    LICENCE_TYPES = [
        ('3CX Standard', '3CX Standard'),
        ('3CX Pro', '3CX Pro'),
        ('3CX Enterprise', '3CX Enterprise'),
    ]
    licence_type = models.CharField(max_length=20, choices=LICENCE_TYPES)

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

