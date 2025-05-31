import csv
from io import StringIO
from django.http import HttpResponse
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError

def validate_emails(raw_emails):
    """
    Takes a comma-separated string of emails.
    Returns a tuple of (valid_emails, invalid_emails).
    """
    raw_list = [e.strip() for e in raw_emails.split(',') if e.strip()]
    valid = []
    invalid = []

    for email in raw_list:
        try:
            django_validate_email(email)
            valid.append(email)
        except ValidationError:
            invalid.append(email)

    return valid, invalid


def generate_csv_for_selected_emails(emails):
    """
    Generates a CSV file response containing the selected emails.
    """
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Email Address"])

    for email in emails:
        writer.writerow([email])

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Client_List.csv'
    return response
