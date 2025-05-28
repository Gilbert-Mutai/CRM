from django.urls import path
from . import views


urlpatterns = [
    path('records/', views.domain_records, name = 'domain_records')
    
]