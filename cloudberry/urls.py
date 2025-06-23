from django.urls import path
from . import views


urlpatterns = [path("records/", views.cloudberry_records, name="cloudberry_records")]
