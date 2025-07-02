from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpResponse
from .models import Veeam
import csv


def get_record_by_id(pk):
    try:
        return Veeam.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None


def delete_record(pk):
    try:
        record = Veeam.objects.get(pk=pk)
        record.delete()
    except Veeam.DoesNotExist:
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


def generate_csv_for_selected_emails(emails):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="emails.csv"'

    writer = csv.writer(response)
    writer.writerow(["Email Address"])
    for email in emails:
        writer.writerow([email])

    return response
