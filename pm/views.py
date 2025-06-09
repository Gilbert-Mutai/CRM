from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .forms import AddProjectForm, UpdateProjectForm
from .utils import (
    get_all_projects, get_project_by_id, delete_project, has_form_changed, generate_csv_for_selected_projects
)
from .models import Project


@login_required
def pm_records(request):
    query = request.GET.get('search', '')
    engineer_filter = request.GET.get('engineer', '')
    status_filter = request.GET.get('status', '')

    projects = get_all_projects()

    if query:
        projects = projects.filter(
            Q(customer_name__name__icontains=query)
        )

    if engineer_filter:
        projects = projects.filter(engineer__id=engineer_filter)

    if status_filter:
        projects = projects.filter(status=status_filter)

    # Pagination
    page_size = request.GET.get('page_size', 20)
    try:
        page_size = int(page_size)
        if page_size not in [20, 50, 100]:
            page_size = 20
    except ValueError:
        page_size = 20

    paginator = Paginator(projects, page_size)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Get list of engineers for filter dropdown
    engineers = Project.objects.values_list('engineer__id', 'engineer__first_name', 'engineer__last_name').distinct()
    engineers_choices = [(e[0], f"{e[1]} {e[2]}") for e in engineers if e[0]]

    context = {
        'projects': page_obj.object_list,
        'page_obj': page_obj,
        'page_size': page_size,
        'search_query': query,
        'selected_engineer': engineer_filter,
        'selected_status': status_filter,
        'engineers': engineers_choices,
        'status_choices': dict(Project.STATUS_CHOICES),
    }
    return render(request, 'pm_records.html', context)


@login_required
def pm_record_details(request, pk):
    project = get_project_by_id(pk)
    return render(request, 'pm_record_details.html', {'project': project})


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
            return redirect('pm_records')
    else:
        form = AddProjectForm()

    return render(request, 'pm_add_record.html', {'form': form})


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
            return redirect('pm_record_details', pk=pk)
    else:
        form = UpdateProjectForm(instance=project)

    return render(request, 'pm_update_record.html', {'form': form, 'project': project})


@login_required
def delete_pm_record(request, pk):
    delete_project(pk)
    messages.success(request, "Project deleted successfully.")
    return redirect('pm_records')


@require_POST
@login_required
def export_selected_pm_records(request):
    project_ids = request.POST.getlist('project_ids')
    return generate_csv_for_selected_projects(project_ids)
