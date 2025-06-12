from django.urls import path
from . import views


urlpatterns = [
    path('records/', views.veeam_records, name = 'veeam_records')
    
]