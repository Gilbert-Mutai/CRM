from django import forms
from .models import SDWAN
from core.models import Client


class ClientNameOnlyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class BaseSDWANForm(forms.ModelForm):
    client = ClientNameOnlyChoiceField(
        queryset=Client.objects.order_by("name"),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_client"}),
        empty_label="Select Client",
    )

    account_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    provider = forms.ChoiceField(
        choices=SDWAN.PROVIDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = SDWAN
        fields = [
            "client",
            "account_number",
            "provider",
        ]


class AddSDWANForm(BaseSDWANForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide labels and use placeholders instead
        for field in self.fields.values():
            field.label = ""
        self.fields["account_number"].widget.attrs["placeholder"] = "Account Number"


class UpdateSDWANForm(BaseSDWANForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show proper labels
        self.fields["client"].label = "Client"
        self.fields["account_number"].label = "Account Number"
        self.fields["provider"].label = "Provider"
