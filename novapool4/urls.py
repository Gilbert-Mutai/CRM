from django.urls import path
from . import views


urlpatterns = [path("records/", views.novapool4_records, name="novapool4_records")]
