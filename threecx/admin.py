from django.contrib import admin
from .models import ThreeCX



@admin.register(ThreeCX)
class ThreeCXAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email_address', 'contact_details', 'sip_provider', 'fqdn', 'license_type', 'created_at', 'last_updated')
    list_filter = ('sip_provider', 'license_type')
    search_fields = ('company_name', 'email_address')
    readonly_fields = ('created_at', 'last_updated')
    
    fieldsets = (
        (None, {
            'fields': ('company_name', 'email_address', 'contact_details', 'sip_provider', 'fqdn', 'license_type')
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

