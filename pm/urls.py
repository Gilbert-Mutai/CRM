from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.pm_records, name='pm_records'),
    path('record/<int:pk>/', views.pm_record_details, name='pm_record'),
    path('delete/<int:pk>/', views.delete_pm_record, name='delete_pm_record'),
    path('add/', views.add_pm_record, name='add_pm_record'),
    path('update/<int:pk>/', views.update_pm_record, name='update_pm_record'),
    path('export/', views.export_selected_pm_records, name='export_selected_pm_records'),
]
