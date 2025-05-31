from django.contrib import admin
from .models import ThreeCX

@admin.register(ThreeCX)
class ThreeCXAdmin(admin.ModelAdmin):
    list_display = (
        'get_client_name', 'get_client_email', 'get_client_phone',
        'sip_provider', 'fqdn', 'license_type',
        'created_at', 'last_updated'
    )
    list_filter = ('sip_provider', 'license_type')
    search_fields = ('client__name', 'client__email', 'client__phone_number')
    readonly_fields = ('created_at', 'last_updated')

    fieldsets = (
        (None, {
            'fields': ('client', 'sip_provider', 'fqdn', 'license_type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated')
        }),
    )

    def get_client_name(self, obj):
        return obj.client.name
    get_client_name.short_description = 'Client Name'

    def get_client_email(self, obj):
        return obj.client.email
    get_client_email.short_description = 'Email Address'

    def get_client_phone(self, obj):
        return obj.client.phone_number
    get_client_phone.short_description = 'Phone Number'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
