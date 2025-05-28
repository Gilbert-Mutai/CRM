from django.urls import path
from . import views


urlpatterns = [
    path('records/', views.pm_records, name = 'pm_records')
    
]