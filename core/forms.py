from django import forms
from .models import Client
from core.utils import validate_emails
from core.constants import SIGNATURE_CHOICES


# Base form shared between Add and Update
class BaseClientForm(forms.ModelForm):
    client_type = forms.ChoiceField(
        choices=Client.CLIENT_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="",
    )

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Full Name or Company", "class": "form-control"}
        ),
        label="",
    )

    contact_person = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Contact Person (for Company)",
                "class": "form-control",
            }
        ),
        label="",
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email Address", "class": "form-control"}
        ),
        label="",
    )

    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Phone Number", "class": "form-control"}
        ),
        label="",
    )

    class Meta:
        model = Client
        fields = ["client_type", "name", "contact_person", "email", "phone_number"]


# Add form
class AddClientForm(BaseClientForm):
    pass


# Update form with optional adjustments
class ClientUpdateForm(BaseClientForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: explicitly remove labels again if needed
        for field in self.fields.values():
            field.label = ""


# Send notifications form


class NotificationForm(forms.Form):
    bcc_emails = forms.CharField(widget=forms.HiddenInput())

    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
        label="",
    )

    signature = forms.ChoiceField(
        choices=SIGNATURE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="",
    )

    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "id": "editor"}), label=""
    )

    def clean_bcc_emails(self):
        raw = self.cleaned_data["bcc_emails"]
        valid_emails, invalid_emails = validate_emails(raw)
        if not valid_emails:
            raise forms.ValidationError("No valid Bcc email addresses provided.")
        self.cleaned_data["valid_emails"] = valid_emails
        self.cleaned_data["invalid_emails"] = invalid_emails
        return raw
