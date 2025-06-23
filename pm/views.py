from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db.models.functions import ExtractYear, ExtractMonth
from django.core.paginator import Paginator
from django.utils.http import urlencode

from .forms import AddProjectForm, UpdateProjectForm
from .models import Project
from .utils import (
    get_project_by_id,
    delete_project,
    has_form_changed,
    generate_csv_for_selected_projects,
)
from django.http import HttpResponse

# Advanced

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


from reportlab.pdfgen import canvas
from io import BytesIO


@login_required
def pm_records(request):
    query = request.GET.get("search", "")
    engineer_filter = request.GET.get("engineer", "")
    status_filter = request.GET.get("status", "")
    certificate_filter = request.GET.get("certificate", "")
    year_filter = request.GET.get("year", "")
    month_filter = request.GET.get("month", "")

    projects = Project.objects.all().order_by("-date_of_request")

    if query:
        projects = projects.filter(
            Q(customer_name__name__icontains=query) | Q(project_title__icontains=query)
        )

    if engineer_filter:
        projects = projects.filter(engineer__id=engineer_filter)

    if status_filter:
        projects = projects.filter(status=status_filter)

    if certificate_filter:
        projects = projects.filter(job_completion_certificate=certificate_filter)

    if year_filter:
        projects = projects.filter(date_of_request__year=year_filter)

    if month_filter:
        projects = projects.filter(date_of_request__month=month_filter)

    # Pagination
    page_size = request.GET.get("page_size", 20)
    try:
        page_size = int(page_size)
        if page_size not in [20, 50, 100]:
            page_size = 20
    except ValueError:
        page_size = 20

    paginator = Paginator(projects, page_size)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Exclude 'page' from querystring
    get_params = request.GET.copy()
    get_params.pop("page", None)
    querystring = get_params.urlencode()

    # Engineer choices
    engineers = Project.objects.values_list(
        "engineer__id", "engineer__first_name", "engineer__last_name"
    ).distinct()
    engineers_choices = [(e[0], f"{e[1]} {e[2]}") for e in engineers if e[0]]

    # Available years for filter
    available_years = (
        Project.objects.annotate(year=ExtractYear("date_of_request"))
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )

    # Available months
    raw_months = (
        Project.objects.annotate(month=ExtractMonth("date_of_request"))
        .values_list("month", flat=True)
        .distinct()
        .order_by("month")
    )
    import calendar
    months = [(m, calendar.month_name[m]) for m in raw_months if m]

    context = {
        "projects": page_obj.object_list,
        "page_obj": page_obj,
        "page_size": page_size,
        "querystring": querystring,
        "search_query": query,
        "selected_engineer": engineer_filter,
        "selected_status": status_filter,
        "selected_certificate": certificate_filter,
        "selected_year": year_filter,
        "selected_month": month_filter,
        "engineers": engineers_choices,
        "status_choices": dict(Project.STATUS_CHOICES),
        "certificate_choices": dict(Project.CERTIFICATE_CHOICES),
        "available_years": available_years,
        "months": months,
    }

    return render(request, "pm_records.html", context)



@login_required
def pm_record_details(request, pk):
    project = get_project_by_id(pk)
    context = {"project": project}

    if request.user.is_staff:
        try:
            engineer_group = Group.objects.get(name="Engineers")
            engineers = engineer_group.user_set.all()
        except Group.DoesNotExist:
            engineers = User.objects.none()

        context["engineers"] = engineers

    return render(request, "pm_record_details.html", context)


@login_required
def add_pm_record(request):
    if request.method == "POST":
        form = AddProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.created_by = request.user
            new_project.updated_by = request.user
            new_project.save()
            messages.success(request, "Project added successfully.")
            return redirect("pm_records")
    else:
        form = AddProjectForm()

    return render(request, "pm_add_record.html", {"form": form})


@login_required
def update_pm_record(request, pk):
    project = get_project_by_id(pk)
    if request.method == "POST":
        form = UpdateProjectForm(request.POST, instance=project)
        if form.is_valid():
            updated_project = form.save(commit=False)
            if has_form_changed(form):
                updated_project.updated_by = request.user
                updated_project.save()
                messages.success(request, "Project updated successfully.")
            else:
                messages.warning(request, "No changes detected.")
            return redirect("pm_record", pk=pk)
    else:
        form = UpdateProjectForm(instance=project)

    return render(request, "pm_update_record.html", {"form": form, "project": project})


@login_required
def delete_pm_record(request, pk):
    delete_project(pk)
    messages.success(request, "Project deleted successfully.")
    return redirect("pm_records")


@require_POST
@login_required
def export_selected_pm_records(request):
    project_ids = request.POST.getlist("project_ids")
    return generate_csv_for_selected_projects(project_ids)


# Advanced Logics


@csrf_exempt
@login_required
def toggle_project_status(request, pk):
    project = get_project_by_id(pk)

    if request.user != project.engineer and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    data = json.loads(request.body)
    new_status = data.get("status")

    project.status = new_status

    if new_status == Project.STATUS_COMPLETED:
        project.date_of_completion = timezone.now()
    else:
        project.date_of_completion = None

    project.updated_by = request.user
    project.save()

    return JsonResponse(
        {
            "status": new_status,
            "status_display": project.get_status_display(),
            "completion_date": (
                project.date_of_completion.strftime("%b %d, %Y %H:%M")
                if project.date_of_completion
                else None
            ),
        }
    )


@csrf_exempt
@login_required
def update_project_engineer(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    data = json.loads(request.body)
    engineer_id = data.get("engineer_id")

    try:
        engineer = User.objects.get(pk=engineer_id)
        project.engineer = engineer
        project.updated_by = request.user
        project.save()
        return JsonResponse({"success": True})
    except User.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Engineer not found"}, status=400
        )


@csrf_exempt
@login_required
def update_project_comment(request, pk):
    project = get_project_by_id(pk)

    if request.user != project.engineer and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    data = json.loads(request.body)
    comment = data.get("comment", "").strip()
    project.comment = comment
    project.updated_by = request.user
    project.save()

    return JsonResponse({"comment": comment})


# views.py
@csrf_exempt
@login_required
def update_project_description(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.engineer and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    data = json.loads(request.body)
    new_desc = data.get("service_description")
    project.service_description = new_desc
    project.updated_by = request.user
    project.save()
    return JsonResponse({"service_description": new_desc})


@login_required
def download_completion_certificate(request, pk):
    project = get_object_or_404(Project, pk=pk)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(
        100, 750, f"Completion Certificate for Project: {project.project_title}"
    )
    p.drawString(100, 730, f"Customer: {project.customer_name.name}")
    p.drawString(100, 710, f"Engineer: {project.engineer.get_full_name()}")
    p.drawString(
        100, 690, f"Completed On: {project.date_of_completion.strftime('%Y-%m-%d')}"
    )
    p.showPage()
    p.save()

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="completion_certificate.pdf"'
    )
    return response


@csrf_exempt
@login_required
def toggle_certificate_status(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.engineer and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    data = json.loads(request.body)
    new_status = data.get("certificate_status")

    project.job_completion_certificate = new_status
    project.save()

    return JsonResponse(
        {
            "certificate_status": new_status,
            "certificate_status_display": project.get_job_completion_certificate_display(),
        }
    )
