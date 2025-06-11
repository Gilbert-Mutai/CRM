from django import forms
from .models import ThreeCX
from core.models import Client


# Custom field to show only client.name
class ClientNameOnlyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AddThreeCXForm(forms.ModelForm):
    client = ClientNameOnlyChoiceField(  # <-- Use custom field here
        queryset=Client.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Client",
        label=""
    )

    sip_provider = forms.ChoiceField(
        choices=ThreeCX.SIP_PROVIDERS,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )

    fqdn = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "FQDN", "class": "form-control"}),
        label=""
    )

    license_type = forms.ChoiceField(
        choices=ThreeCX.LICENSE_TYPES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )

    class Meta:
        model = ThreeCX
        fields = ['client', 'fqdn', 'sip_provider', 'license_type']


class Update3CXForm(forms.ModelForm):
    class Meta:
        model = ThreeCX
        fields = [
            'client',
            'sip_provider',
            'fqdn',
            'license_type',
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'sip_provider': forms.Select(attrs={'class': 'form-control'}),
            'fqdn': forms.TextInput(attrs={'class': 'form-control'}),
            'license_type': forms.Select(attrs={'class': 'form-control'}),
        }
