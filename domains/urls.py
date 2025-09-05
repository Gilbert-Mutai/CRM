from django.urls import path
from . import views


urlpatterns = [
    # Domain Records
    path("records/", views.domain_records, name="domain_records"),
    path("record/<int:pk>/", views.domain_record_details, name="domain_record"),
    path("delete/<int:pk>/", views.delete_domain_record, name="delete_domain_record"),
    path("add/", views.add_domain_record, name="add_domain_record"),
    path("update/<int:pk>/", views.update_domain_record, name="update_domain_record"),
    path(
        "send-notification/",
        views.send_notification_domain,
        name="send_notification_domain",
    ),
    path(
        "export/",
        views.export_selected_domain_records,
        name="export_selected_domain_records",
    ),
]
