from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.core.paginator import Paginator
from .utils import generate_csv_for_selected_emails
from django.views.decorators.http import require_POST
from .models import Client
from .forms import AddClientForm, ClientUpdateForm, NotificationForm
from core.constants import SIGNATURE_BLOCKS as SIGNATURES


def home(request):
    return render(request, "home.html")


@login_required
def access_center(request):
    client_sections = [
        {
            "title": "3CX",
            "url_name": "threecx_records",
            "icon": "telephone",
            "btn_class": "primary",
        },
        {
            "title": "Domain & Hosting",
            "url_name": "domain_records",
            "icon": "globe",
            "btn_class": "success",
        },
        {
            "title": "Nova",
            "url_name": "nova_records",
            "icon": "lightning-charge",
            "btn_class": "warning",
        },
        {
            "title": "Cloudberry",
            "url_name": "cloudberry_records",
            "icon": "cloud",
            "btn_class": "danger",
        },
        {
            "title": "Novapool 4",
            "url_name": "novapool4_records",
            "icon": "cpu",
            "btn_class": "warning",
        },
        {
            "title": "SD-WAN",
            "url_name": "sdwan_records",
            "icon": "diagram-3",
            "btn_class": "primary",
        },

        {
            "title": "Veeam",
            "url_name": "veeam_records",
            "icon": "shield-check",
            "btn_class": "success",
        },
        {
            "title": "Project",
            "url_name": "pm_records",
            "icon": "kanban",
            "btn_class": "danger",
        },
    ]
    return render(request, "access_center.html", {"client_sections": client_sections})


@login_required
def client_records(request):
    query = request.GET.get("search", "").strip()
    selected_client_type = request.GET.get("client_type", "").strip()

    # Base queryset
    clients = Client.objects.all().order_by("-last_updated", "-created_at")

    # Filters
    if query:
        clients = clients.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(contact_person__icontains=query)
        )
    if selected_client_type:
        clients = clients.filter(client_type=selected_client_type)

    # Unique client types for filter dropdown
    client_types = Client.objects.values_list("client_type", flat=True).distinct()

    # Handle page size (with safe fallback)
    page_size = request.GET.get("page_size", 20)
    try:
        page_size = int(page_size)
        if page_size not in [20, 50, 100]:
            page_size = 20
    except ValueError:
        page_size = 20

    # Pagination
    paginator = Paginator(clients, page_size)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Preserve other query parameters in pagination links
    get_params = request.GET.copy()
    get_params["page_size"] = str(page_size)
    if "page" in get_params:
        del get_params["page"]

    context = {
        "clients": page_obj,      
        "page_size": page_size,
        "search_query": query,
        "client_types": client_types,
        "selected_client_type": selected_client_type,
        "querystring": get_params.urlencode(),    
    }

    return render(request, "client_records.html", context)



@login_required
def client_record(request, pk):
    client_record = get_object_or_404(Client, pk=pk)
    return render(
        request, "client_record_details.html", {"client_record": client_record}
    )


@login_required
def add_client_record(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.created_by = request.user
            new_client.updated_by = request.user
            new_client.save()
            messages.success(request, "Client added successfully.")
            return redirect("client_records")
    else:
        form = AddClientForm()

    return render(request, "client_add_record.html", {"form": form})


@login_required
def update_client_record(request, pk):
    client_record = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientUpdateForm(request.POST, instance=client_record)
        if form.is_valid():
            if form.has_changed():
                updated_client = form.save(commit=False)
                updated_client.updated_by = request.user
                updated_client.save()
                messages.success(request, "Client updated successfully.")
            else:
                messages.warning(request, "No changes detected.")
            return redirect("client_record", pk=client_record.pk)
    else:
        form = ClientUpdateForm(instance=client_record)

    return render(
        request,
        "client_update_record.html",
        {"form": form, "client_record": client_record},
    )


def delete_client_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to do that.")
        return redirect("login")

    if request.method == "POST":
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect("client_records")

    messages.error(request, "Invalid request. Deletion only allowed via POST.")
    return redirect("client_record", pk=pk)


@login_required
def send_notification_client(request):
    if request.method == "GET":
        emails_param = request.GET.get("emails", "")
        emails = [e for e in emails_param.split(",") if e]
        if not emails:
            messages.error(request, "No email addresses provided.")
            return redirect("client_records")
        form = NotificationForm(initial={"bcc_emails": ",".join(emails)})
        return render(
            request, "client_email_notification.html", {"form": form, "emails": emails}
        )

    if request.method == "POST":
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
            return redirect("client_records")
        else:
            # Retain visible email list in form reshow
            emails = request.POST.get("bcc_emails", "").split(",")
            return render(
                request,
                "client_email_notification.html",
                {"form": form, "emails": emails},
            )

    return redirect("client_records")


@require_POST
@login_required
def export_clients(request):
    emails = request.POST.get("emails", "").split(",")
    return generate_csv_for_selected_emails(emails)
