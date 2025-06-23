from django.urls import path
from . import views


urlpatterns = [path("records/", views.sdwan_records, name="sdwan_records")]
