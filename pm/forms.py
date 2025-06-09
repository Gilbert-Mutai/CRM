from django import forms
from core.models import Client
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Project

class AddProjectForm(forms.ModelForm):
    customer_name = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Client",
        label=""
    )

    status = forms.ChoiceField(
        choices=Project.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=""
    )

    job_completion_certificate = forms.ChoiceField(
        choices=Project.CERTIFICATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=""
    )

    engineer = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Engineers'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="",
        required=False,
    )

    date_of_completion = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'  # HTML5 datetime picker
        }),
        required=False,
        label=""
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label=""
    )

    service_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label=""
    )

    class Meta:
        model = Project
        fields = [
            'customer_name',
            'service_description',
            'status',
            'date_of_completion',
            'job_completion_certificate',
            'engineer',
            'comment',
        ]


class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'customer_name',
            'service_description',
            'status',
            'date_of_completion',
            'job_completion_certificate',
            'engineer',
            'comment',
        ]
        widgets = {
            'customer_name': forms.Select(attrs={'class': 'form-control'}),
            'service_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date_of_completion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'job_completion_certificate': forms.Select(attrs={'class': 'form-control'}),
            'engineer': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
