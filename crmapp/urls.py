from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    
    path('set-password/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),
    
    # Reset password paths
    
    
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ),  name='password_reset'),


    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ),  name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ),  name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ),  name='password_reset_complete'),
    
    # 3CX Records
    path('3cx-records/', views.threecx_records, name='threecx_records'),
    path('3cx-record/<int:pk>/', views.threecx_record_details, name='threecx_record'),
    path('3cx-delete/<int:pk>/', views.delete_threecx_record, name='delete_threecx_record'),
    path('3cx-add/', views.add_threecx_record, name='add_threecx_record'),
    path('3cx-update/<int:pk>/', views.update_threecx_record, name='update_threecx_record'),
    
    path('compose-email/', views.compose_email, name='compose_email'),
    
]

