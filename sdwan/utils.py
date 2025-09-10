from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpResponse
from .models import SDWAN
import csv


def get_record_by_id(pk):
    """Fetch a single SD-WAN record by primary key."""
    try:
        return SDWAN.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None


def delete_record(pk):
    """Delete a single SD-WAN record by primary key."""
    try:
        record = SDWAN.objects.get(pk=pk)
        record.delete()
    except SDWAN.DoesNotExist:
        pass


def validate_emails(emails):
    """Validate a list of emails and split into valid/invalid lists."""
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    valid_emails = []
    invalid_emails = []

    for email in emails:
        try:
            validate_email(email)
            valid_emails.append(email)
        except ValidationError:
            invalid_emails.append(email)

    return valid_emails, invalid_emails


def has_form_changed(form):
    """Check if a form has unsaved changes."""
    return form.has_changed()
