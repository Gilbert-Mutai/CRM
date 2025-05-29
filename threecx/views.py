# Updated threecx/views.py to support search and filter functionality
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import AddThreeCXForm
from .utils import get_record_by_id, delete_record, validate_emails, has_form_changed,generate_csv_for_selected_emails
from .models import ThreeCX
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

def threecx_records(request):
    query = request.GET.get('search', '')
    sip_filter = request.GET.get('sip_provider', '')
    license_filter = request.GET.get('license_type', '')

    records = ThreeCX.objects.all().order_by('-last_updated', '-created_at')

    if query:
        records = records.filter(
            Q(company_name__icontains=query) |
            Q(email_address__icontains=query) |
            Q(fqdn__icontains=query)
        )

    if sip_filter:
        records = records.filter(sip_provider=sip_filter)

    if license_filter:
        records = records.filter(license_type=license_filter)

    # Pagination logic
    page_size = request.GET.get('page_size', 20)
    try:
        page_size = int(page_size)
        if page_size not in [20, 50, 100]:
            page_size = 20
    except ValueError:
        page_size = 20

    paginator = Paginator(records, page_size)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'records': page_obj.object_list,
        'page_obj': page_obj,  # the paginated page
        'page_size': page_size,
        'search_query': query,
        'selected_sip': sip_filter,
        'sip_providers': dict(ThreeCX.SIP_PROVIDERS),
        'license_types': dict(ThreeCX.LICENSE_TYPES),

    }
    return render(request, 'threecx_records.html', context)


def threecx_record_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view that page.")
        return redirect('home')

    customer_record = get_record_by_id(pk)
    return render(request, 'threecx_record_details.html', {'customer_record': customer_record})


def delete_threecx_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to do that.")
        return redirect('login')

    delete_record(pk)
    messages.success(request, "Record deleted successfully.")
    return redirect('threecx_records')


def add_threecx_record(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in.")
        return redirect('login')

    if request.method == "POST":
        form = AddThreeCXForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.created_by = request.user
            new_record.updated_by = request.user
            new_record.save()
            messages.success(request, "Record has been added!")
            return redirect('threecx_records')
    else:
        form = AddThreeCXForm()

    return render(request, 'threecx_add_record.html', {'form': form})

def update_threecx_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in.")
        return redirect('login')

    current_record = get_record_by_id(pk)
    form = AddThreeCXForm(request.POST or None, instance=current_record)

    if form.is_valid():
        updated_record = form.save(commit=False)

        if has_form_changed(form):
            updated_record.updated_by = request.user
            updated_record.save()
            messages.success(request, "Record has been updated!")
        else:
            messages.warning(request, "No changes detected.")

        return redirect('threecx_record', pk=pk)

    return render(request, 'threecx_update_record.html', {
        'form': form,
        'customer_record': current_record
    })

@login_required
def send_notification(request):
    if request.method == "POST":
        raw_emails = request.POST.get('emails', '')

        valid_emails, invalid_emails = validate_emails(raw_emails)

        if invalid_emails:
            messages.warning(request, f"The following email(s) are invalid and will be ignored: {', '.join(invalid_emails)}")

        if not valid_emails:
            messages.error(request, "No valid email addresses found. Please enter at least one valid email.")
            return redirect('threecx_records')

        return render(request, 'threecx_email_notification.html', {'emails': valid_emails})

    return redirect('threecx_records')


@require_POST
@login_required
def export_selected_records(request):
    emails = request.POST.get('emails', '').split(',')
    return generate_csv_for_selected_emails(emails)
