from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import SignUpForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = SignUpForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
# Register the CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

