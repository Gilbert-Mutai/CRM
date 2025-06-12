from django import forms
from .models import ThreeCX
from core.models import Client

# Custom field to display only the client name
class ClientNameOnlyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


# Shared base form for ThreeCX
class BaseThreeCXForm(forms.ModelForm):
    client = ClientNameOnlyChoiceField(
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
        widget=forms.TextInput(attrs={
            "placeholder": "FQDN",
            "class": "form-control"
        }),
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


# Add form inherits from base
class AddThreeCXForm(BaseThreeCXForm):
    pass


# Update form inherits from base and modifies if needed
class UpdateThreeCXForm(BaseThreeCXForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optionally ensure labels are hidden
        for field in self.fields.values():
            field.label = ""

