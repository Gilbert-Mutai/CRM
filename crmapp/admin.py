from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ThreeCX
from .forms import SignUpForm

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

@admin.register(ThreeCX)
class ThreeCXAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email_address', 'contact_details', 'sip_provider', 'fqdn', 'licence_type', 'created_at', 'last_updated')
    list_filter = ('sip_provider', 'licence_type')
    search_fields = ('company_name', 'email_address')
    readonly_fields = ('created_at', 'last_updated')
    
    fieldsets = (
        (None, {
            'fields': ('company_name', 'email_address', 'contact_details', 'sip_provider', 'fqdn', 'licence_type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

# Register the CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
