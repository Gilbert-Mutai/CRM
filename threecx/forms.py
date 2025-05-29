from django import forms
from .models import ThreeCX

class AddThreeCXForm(forms.ModelForm):
    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Company Name", "class": "form-control"}),
        label=""
    )
    email_address = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email Address", "class": "form-control"}),
        label=""
    )
    contact_details = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Contact Details", "class": "form-control"}),
        label=""
    )
    fqdn = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "FQDN", "class": "form-control"}),
        label=""
    )
    sip_provider = forms.ChoiceField(
        choices=ThreeCX.SIP_PROVIDERS,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )
    license_type = forms.ChoiceField(
        choices=ThreeCX.LICENSE_TYPES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )

    class Meta:
        model = ThreeCX
        fields = [
            'company_name',
            'email_address',
            'contact_details',
            'fqdn',
            'sip_provider',
            'license_type',
        ]
