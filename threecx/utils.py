from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import ThreeCX
import csv
from io import StringIO
from django.http import HttpResponse
import re


def get_all_records():
    return ThreeCX.objects.all().order_by("-last_updated", "-created_at")


def get_record_by_id(pk):
    return get_object_or_404(ThreeCX, id=pk)


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


def generate_csv_for_selected_emails(emails):
    # Filter via related Client's email field
    records = ThreeCX.objects.filter(client__email__in=emails)

    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(
        ["Name", "Email", "Phone Number", "SIP Provider", "FQDN", "License Type"]
    )

    for rec in records:
        writer.writerow(
            [
                rec.client.name,
                rec.client.email,
                rec.client.phone_number,
                rec.get_sip_provider_display(),
                rec.fqdn,
                rec.get_license_type_display(),
            ]
        )

    csv_content = csv_buffer.getvalue()
    csv_buffer.close()

    response = HttpResponse(csv_content, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="3cx_List.csv"'
    return response
