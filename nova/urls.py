from django.urls import path
from . import views


urlpatterns = [path("records/", views.nova_records, name="nova_records")]
