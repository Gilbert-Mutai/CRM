from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'get_customer_name', 'get_customer_email', 'project_title',
        'status','job_completion_certificate', 'get_engineer_name'
    )
    list_filter = ('status', 'job_completion_certificate')
    search_fields = ('customer_name__name', 'customer_name__email', 'project_title')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    fieldsets = (
        ('Project Info', {
            'fields': (
                'customer_name', 'project_title', 'service_description',
                'status', 'date_of_completion', 'job_completion_certificate',
                'engineer', 'comment'
            )
        }),
        ('Metadata', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at')
        }),
    )

    def get_customer_name(self, obj):
        return obj.customer_name.name
    get_customer_name.short_description = 'Customer Name'

    def get_customer_email(self, obj):
        return obj.customer_name.email
    get_customer_email.short_description = 'Email Address'

    def get_engineer_name(self, obj):
        return obj.engineer.get_full_name() if obj.engineer else "-"
    get_engineer_name.short_description = 'Engineer'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
