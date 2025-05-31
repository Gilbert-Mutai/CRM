from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.core.paginator import Paginator
from .utils import validate_emails, generate_csv_for_selected_emails
from django.views.decorators.http import require_POST
from .models import Client
from .forms import AddClientForm, ClientUpdateForm

def home(request):
    return render(request, 'home.html')

@login_required
def menu(request):
    client_sections = [
        {"title": "3CX", "url_name": "threecx_records", "icon": "telephone", "btn_class": "primary"},
        {"title": "Domain & Hosting", "url_name": "domain_records", "icon": "globe", "btn_class": "success"},
        {"title": "Nova", "url_name": "nova_records", "icon": "lightning-charge", "btn_class": "warning"},
        {"title": "Novapool 4", "url_name": "novapool4_records", "icon": "cpu", "btn_class": "warning"},
        {"title": "SD-WAN", "url_name": "sdwan_records", "icon": "diagram-3", "btn_class": "primary"},
        {"title": "Project Manager", "url_name": "pm_records", "icon": "kanban", "btn_class": "info"},
    ]
    return render(request, 'menu.html', {'client_sections': client_sections})

@login_required
def client_records(request):
    # Extract filters
    query = request.GET.get('search', '').strip()
    selected_client_type = request.GET.get('client_type', '').strip()

    # Initial queryset
    clients = Client.objects.all().order_by('-last_updated', '-created_at')

    # Apply search filter (name, email, contact person)
    if query:
        clients = clients.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(contact_person__icontains=query)
        )

    # Apply client type filter
    if selected_client_type:
        clients = clients.filter(client_type=selected_client_type)

    # Get unique client types for filter dropdown
    client_types = Client.objects.values_list('client_type', flat=True).distinct()

    # Pagination
    page_size = request.GET.get('page_size', 20)
    try:
        page_size = int(page_size)
        if page_size not in [20, 50, 100]:
            page_size = 20
    except ValueError:
        page_size = 20

    paginator = Paginator(clients, page_size)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'clients': page_obj.object_list,
        'page_obj': page_obj,
        'page_size': page_size,
        'search_query': query,
        'client_types': client_types,
        'selected_client_type': selected_client_type,
    }

    return render(request, 'client_records.html', context)

@login_required
def client_record(request, pk):
    client_record = get_object_or_404(Client, pk=pk)
    return render(request, 'client_record_details.html', {'client_record': client_record})


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
            return redirect('client_records')
    else:
        form = AddClientForm()

    return render(request, 'client_add_record.html', {'form': form})

@login_required
def update_client_record(request, pk):
    client_record = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, instance=client_record)
        if form.is_valid():
            updated_client = form.save(commit=False)
            updated_client.updated_by = request.user
            updated_client.save()
            messages.success(request, "Client updated successfully.")
            return redirect('client_record', pk=client_record.pk)
    else:
        form = ClientUpdateForm(instance=client_record)

    return render(request, 'client_update_record.html', {'form': form, 'client_record': client_record})

def delete_client_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to do that.")
        return redirect('login')

    if request.method == "POST":
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect('client_records')

    messages.error(request, "Invalid request. Deletion only allowed via POST.")
    return redirect('client_record', pk=pk)

@login_required
def send_notification(request):
    if request.method == "GET":
        emails_param = request.GET.get('emails', '')
        emails = [e for e in emails_param.split(',') if e]
        if not emails:
            messages.error(request, "No email addresses provided.")
            return redirect('client_records')
        return render(request, 'client_email_notification.html', {'emails': emails})

    if request.method == "POST" and 'emails' in request.POST:
        raw_emails = request.POST.get('emails', '')
        valid_emails, invalid_emails = validate_emails(raw_emails)

        if invalid_emails:
            messages.warning(request, f"Ignoring invalid email(s): {', '.join(invalid_emails)}")

        if not valid_emails:
            messages.error(request, "No valid email addresses found.")
            return redirect('client_records')

        return render(request, 'client_email_notification.html', {'emails': valid_emails})

    if request.method == "POST" and 'bcc_emails' in request.POST:
        bcc_raw = request.POST.get('bcc_emails', '')
        valid_emails, invalid_emails = validate_emails(bcc_raw)

        if invalid_emails:
            messages.warning(request, f"Ignoring invalid Bcc email(s): {', '.join(invalid_emails)}")

        if not valid_emails:
            messages.error(request, "No valid Bcc email addresses to send.")
            return redirect('client_records')

        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        signature = request.POST.get('signature', '').strip()

        full_body = f"{body}<br><br>Regards,<br><strong>{signature}</strong>"

        msg = EmailMultiAlternatives(
            subject=subject,
            body=full_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            bcc=valid_emails,
        )
        msg.attach_alternative(full_body, "text/html")
        msg.send(fail_silently=False)

        messages.success(request, f"Notification sent to {len(valid_emails)} recipient(s).")
        return redirect('client_records')

    return redirect('client_records')

@require_POST
@login_required
def export_clients(request):
    emails = request.POST.get('emails', '').split(',')
    return generate_csv_for_selected_emails(emails)
