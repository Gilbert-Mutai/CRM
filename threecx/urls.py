from django.urls import path
from . import views


urlpatterns = [
    # 3CX Records
    path("records/", views.threecx_records, name="threecx_records"),
    path("record/<int:pk>/", views.threecx_record_details, name="threecx_record"),
    path("delete/<int:pk>/", views.delete_threecx_record, name="delete_threecx_record"),
    path("add/", views.add_threecx_record, name="add_threecx_record"),
    path("update/<int:pk>/", views.update_threecx_record, name="update_threecx_record"),
    path(
        "send-notification/",
        views.send_notification_threecx,
        name="send_notification_threecx",
    ),
    path(
        "export/",
        views.export_selected_threecx_records,
        name="export_selected_threecx_records",
    ),
]
