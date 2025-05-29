from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # 3CX Records
    path('records/', views.threecx_records, name='threecx_records'),
    path('record/<int:pk>/', views.threecx_record_details, name='threecx_record'),
    path('delete/<int:pk>/', views.delete_threecx_record, name='delete_threecx_record'),
    path('add/', views.add_threecx_record, name='add_threecx_record'),
    path('update/<int:pk>/', views.update_threecx_record, name='update_threecx_record'),
    
    path('send-notification/', views.send_notification, name='send_notification'),
    
    path('export/', views.export_selected_records, name='export_selected_records'),

    
]

