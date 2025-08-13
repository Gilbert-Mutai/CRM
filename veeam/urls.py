from django.urls import path
from . import views


urlpatterns = [
    path("records/", views.veeam_records, name="veeam_records"),
    path("record/<int:pk>/", views.veeam_record_details, name="veeam_record"),
    path("delete/<int:pk>/", views.delete_veeam_record, name="delete_veeam_record"),
    path("add/", views.add_veeam_record, name="add_veeam_record"),
    path("update/<int:pk>/", views.update_veeam_record, name="update_veeam_record"),
    path(
        "send-notification/",
        views.send_notification_veeam,
        name="send_notification_veeam",
    ),
    path("export/", views.export_selected_records, name="export_selected_records"),
    path('record/<int:pk>/tag/', views.update_veeam_tag, name='update_veeam_tag'),
    path('record/<int:pk>/status/', views.update_veeam_status, name='update_veeam_status'),
    path('record/<int:pk>/comment/', views.update_veeam_comment, name='update_veeam_comment')


]
