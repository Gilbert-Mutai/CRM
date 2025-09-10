from django.shortcuts import get_object_or_404
from .models import Project
import csv
from io import StringIO
from django.http import HttpResponse

def get_project_by_id(pk):
    return Project.objects.select_related("engineer", "customer_name").get(pk=pk)


def delete_project(pk):
    project = get_project_by_id(pk)
    project.delete()


def has_form_changed(form, instance=None):
    return form.has_changed()


def generate_csv_for_selected_projects(project_ids):
    projects = Project.objects.filter(id__in=project_ids)

    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(
        [
            "Customer Name",
            "Service Description",
            "Status",
            "Date of Request",
            "Date of Completion",
            "Job Completion Certificate",
            "Engineer",
            "Comment",
        ]
    )

    for p in projects:
        writer.writerow(
            [
                p.customer_name.name if p.customer_name else "",
                p.service_description,
                p.status,
                p.date_of_request.strftime("%Y-%m-%d %H:%M"),
                (
                    p.date_of_completion.strftime("%Y-%m-%d %H:%M")
                    if p.date_of_completion
                    else ""
                ),
                p.job_completion_certificate,
                p.engineer.get_full_name() if p.engineer else "",
                p.comment,
            ]
        )

    csv_content = csv_buffer.getvalue()
    csv_buffer.close()

    response = HttpResponse(csv_content, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="project_list.csv"'
    return response
