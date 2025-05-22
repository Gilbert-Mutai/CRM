from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('records/', views.customer_records, name='records'),
    
    path('set-password/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),
    
]

