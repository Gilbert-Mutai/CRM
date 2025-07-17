from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .forms import AddVeeamForm, UpdateVeeamForm
from .models import VeeamJob
from core.models import Client
import csv
from django.http import HttpResponse
from .utils import (
    get_record_by_id,
    delete_record,
    has_form_changed,
)
from core.forms import NotificationForm
from core.constants import SIGNATURE_BLOCKS as SIGNATURES


@login_required
def veeam_records(request):
    query = request.GET.get("search", "")
    site_filter = request.GET.get("site", "")
    os_filter = request.GET.get("os", "")
    status_filter = request.GET.get("job_status", "")

    records = VeeamJob.objects.select_related("client").order_by(
        "client__name", "client__email", "id"
    )

    if query:
        records = records.filter(
            Q(client__name__icontains=query) | Q(computer_name__icontains=query)
        )

    if site_filter:
        records = records.filter(site=site_filter)

    if os_filter:
        records = records.filter(os=os_filter)

    if status_filter:
        records = records.filter(job_status=status_filter)

    page_size = request.GET.get("page_size", 20)
    try:
        page_size = int(page_size)
        if page_size not in [20, 50, 100]:
            page_size = 20
    except ValueError:
        page_size = 20

    paginator = Paginator(records, page_size)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "records": page_obj.object_list,
        "page_obj": page_obj,
        "page_size": page_size,
        "search_query": query,
        "selected_site": site_filter,
        "selected_os": os_filter,
        "selected_status": status_filter,
        "site_choices": dict(VeeamJob.SITE_CHOICES),
        "os_choices": dict(VeeamJob.OS_CHOICES),
        "status_choices": dict(VeeamJob.JOB_STATUS_CHOICES),
    }

    return render(request, "veeam_records.html", context)


@login_required
def veeam_record_details(request, pk):
    customer_record = get_record_by_id(pk)
    return render(
        request, "veeam_record_details.html", {"customer_record": customer_record}
    )


@login_required
def delete_veeam_record(request, pk):
    delete_record(pk)
    messages.success(request, "Record deleted successfully.")
    return redirect("veeam_records")


@login_required
def add_veeam_record(request):
    if request.method == "POST":
        form = AddVeeamForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.created_by = request.user
            new_record.updated_by = request.user
            new_record.save()
            messages.success(request, "Record has been added!")
            return redirect("veeam_records")
    else:
        form = AddVeeamForm()

    return render(request, "veeam_add_record.html", {"form": form})


@login_required
def update_veeam_record(request, pk):
    current_record = get_record_by_id(pk)
    form = UpdateVeeamForm(request.POST or None, instance=current_record)

    if form.is_valid():
        updated_record = form.save(commit=False)
        if has_form_changed(form):
            updated_record.updated_by = request.user
            updated_record.save()
            messages.success(request, "Record has been updated!")
        else:
            messages.warning(request, "No changes detected.")
        return redirect("veeam_record", pk=pk)

    return render(
        request,
        "veeam_update_record.html",
        {"form": form, "customer_record": current_record},
    )


@login_required
def send_notification_veeam(request):
    if request.method == "GET":
        company_ids_param = request.GET.get("companies", "")
        company_ids = [
            int(cid) for cid in company_ids_param.split(",") if cid.isdigit()
        ]

        if not company_ids:
            messages.error(request, "No companies selected.")
            return redirect("veeam_records")

        # Get clients and emails
        clients = Client.objects.filter(id__in=company_ids)
        emails = [client.email for client in clients if client.email]

        if not emails:
            messages.error(request, "Selected companies have no valid emails.")
            return redirect("veeam_records")

        form = NotificationForm(initial={"bcc_emails": ",".join(emails)})
        return render(
            request, "veeam_email_notification.html", {"form": form, "emails": emails}
        )

    elif request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            body = form.cleaned_data["body"]
            signature_key = form.cleaned_data["signature"]
            valid_emails = form.cleaned_data["valid_emails"]
            invalid_emails = form.cleaned_data["invalid_emails"]

            if invalid_emails:
                messages.warning(
                    request, f"Ignoring invalid email(s): {', '.join(invalid_emails)}"
                )

            signature_block = SIGNATURES.get(signature_key, signature_key)
            full_body = f"{body}<br><br>--<br>{signature_block}"

            msg = EmailMultiAlternatives(
                subject=subject,
                body=full_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                bcc=valid_emails,
            )
            msg.attach_alternative(full_body, "text/html")
            msg.send(fail_silently=False)

            messages.success(
                request, f"Notification sent to {len(valid_emails)} recipient(s)."
            )
            return redirect("veeam_records")

        emails = request.POST.get("bcc_emails", "").split(",")
        return render(
            request, "veeam_email_notification.html", {"form": form, "emails": emails}
        )

    return redirect("veeam_records")


@require_POST
@login_required
def export_selected_records(request):
    company_ids = request.POST.get("companies", "").split(",")
    company_ids = [cid.strip() for cid in company_ids if cid.strip().isdigit()]
    companies = Client.objects.filter(id__in=company_ids)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Veeam_companies.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "ID", "Company Name", "Email", "Phone", "Contact Person", "Created on", "Last Updated"
    ])

    for company in companies:
        writer.writerow([
            company.id,
            company.name,
            company.email,
            company.phone_number if hasattr(company, 'phone_number') else "",
            company.contact_person if hasattr(company, 'contact_person') else "",
            company.created_at.strftime('%Y-%m-%d') if hasattr(company, 'created_at') else "",
            company.last_updated.strftime('%Y-%m-%d') if hasattr(company, 'last_updated') else "",
        ])

    return response
