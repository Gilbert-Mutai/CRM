from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import ThreeCX
import csv
from io import StringIO
from django.http import HttpResponse


def get_all_records():
    return ThreeCX.objects.all().order_by('-last_updated', '-created_at')

def get_record_by_id(pk):
    return get_object_or_404(ThreeCX, id=pk)

def delete_record(pk):
    record = get_record_by_id(pk)
    record.delete()

def validate_emails(raw_emails: str):
    raw_emails_list = [email.strip() for email in raw_emails.split(',') if email.strip()]

    valid_emails = []
    invalid_emails = []

    for email in raw_emails_list:
        try:
            validate_email(email)
            valid_emails.append(email)
        except ValidationError:
            invalid_emails.append(email)

    return valid_emails, invalid_emails

def has_form_changed(form, instance=None):
    return form.has_changed()



def generate_csv_for_selected_emails(emails):
    records = ThreeCX.objects.filter(email_address__in=emails)

    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(['Company Name', 'Email', 'Contact Details', 'SIP Provider', 'FQDN', 'License Type'])

    for rec in records:
        writer.writerow([
            rec.company_name,
            rec.email_address,
            rec.contact_details,
            rec.get_sip_provider_display(),
            rec.fqdn,
            rec.get_license_type_display(),
        ])

    csv_content = csv_buffer.getvalue()
    csv_buffer.close()

    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="3cx_records.csv"'
    return response

