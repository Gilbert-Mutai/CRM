from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpResponse
from .models import VeeamJob
import csv


def get_record_by_id(pk):
    try:
        return VeeamJob.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None


def delete_record(pk):
    try:
        record = VeeamJob.objects.get(pk=pk)
        record.delete()
    except VeeamJob.DoesNotExist:
        pass


def validate_emails(emails):
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
    return form.has_changed()
