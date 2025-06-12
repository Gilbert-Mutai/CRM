from django import forms
from django.contrib.auth import get_user_model
from core.models import Client
from .models import Project

User = get_user_model()


# Custom field to display only the client name
class ClientNameOnlyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


# Custom field to display engineer's full name
class EngineerNameOnlyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username or obj.email


# Shared Base Form
class BaseProjectForm(forms.ModelForm):
    customer_name = ClientNameOnlyChoiceField(
        queryset=Client.objects.order_by('name'),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_customer_name'  # Needed for Select2 targeting
        }),
        empty_label="Select Client",
        label=""
    )

    project_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Project Title'
        }),
        label=""
    )

    service_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Service Description'
        }),
        label=""
    )

    status = forms.ChoiceField(
        choices=[('', 'Project Status')] + list(Project.STATUS_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=""
    )

    job_completion_certificate = forms.ChoiceField(
        choices=[('', 'Certificate Status')] + list(Project.CERTIFICATE_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=""
    )

    engineer = EngineerNameOnlyChoiceField(
        queryset=User.objects.filter(groups__name='Engineers'),
        empty_label="Select Engineer",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_engineer' 
        }),
        required=False,
        label=""
    )

    date_of_completion = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=False,
        label=""
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Comment'
        }),
        required=False,
        label=""
    )

    class Meta:
        model = Project
        fields = [
            'customer_name',
            'project_title',
            'service_description',
            'status',
            'date_of_completion',
            'job_completion_certificate',
            'engineer',
            'comment',
        ]


class AddProjectForm(BaseProjectForm):
    pass


class UpdateProjectForm(BaseProjectForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide all labels (if needed)
        for field in self.fields.values():
            field.label = ""
