from django.urls import path
from . import views


urlpatterns = [
    path("records/", views.sdwan_records, name="sdwan_records"),
    path("record/<int:pk>/", views.sdwan_record_details, name="sdwan_record"),
    path("delete/<int:pk>/", views.delete_sdwan_record, name="delete_sdwan_record"),
    path("add/", views.add_sdwan_record, name="add_sdwan_record"),
    path("update/<int:pk>/", views.update_sdwan_record, name="update_sdwan_record"),
    path("send-notification/", views.send_notification_sdwan, name="send_notification_sdwan"),
    path("export/", views.export_selected_sdwan_records, name="export_selected_sdwan_records"),
]
