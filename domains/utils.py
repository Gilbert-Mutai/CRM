from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import Domain
import csv
from io import StringIO
from django.http import HttpResponse
import re


def get_all_records():
    return Domain.objects.all().order_by("-updated_on", "-created_on")


def get_record_by_id(pk):
    return get_object_or_404(Domain, id=pk)


def delete_record(pk):
    record = get_record_by_id(pk)
    record.delete()


def validate_emails(raw_emails: str):
    emails = [e.strip() for e in raw_emails.split(",") if e.strip()]
    valid = []
    invalid = []
    for email in emails:
        try:
            validate_email(email)
            valid.append(email)
        except ValidationError:
            invalid.append(email)
    return valid, invalid


def has_form_changed(form, instance=None):
    return form.has_changed()
