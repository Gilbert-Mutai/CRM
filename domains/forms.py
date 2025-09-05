from django import forms
from .models import Domain
from core.models import Client


class ClientNameOnlyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class BaseDomainForm(forms.ModelForm):
    client = ClientNameOnlyChoiceField(
        queryset=Client.objects.order_by("name"),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_client"}),
        empty_label="Select Client",
    )

    class Meta:
        model = Domain
        fields = ["client", "domain", "host", "package", "status"]  # 👈 added status
        widgets = {
            "domain": forms.TextInput(
                attrs={"class": "form-control", "id": "id_domain"}
            ),
            "host": forms.Select(attrs={"class": "form-control", "id": "id_host"}),
            "package": forms.NumberInput(
                attrs={"class": "form-control", "id": "id_package"}
            ),
            "status": forms.Select(
                attrs={"class": "form-control", "id": "id_status"}
            ),  # 👈 dropdown
        }


class AddDomainForm(BaseDomainForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove labels, add placeholders
        self.fields["client"].label = ""
        self.fields["domain"].label = ""
        self.fields["host"].label = ""
        self.fields["package"].label = ""
        self.fields["status"].label = ""  # 👈 added

        self.fields["domain"].widget.attrs["placeholder"] = "Domain"
        self.fields["package"].widget.attrs["placeholder"] = "Package"
        # No placeholder for status since it’s a dropdown


class UpdateDomainForm(BaseDomainForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Use labels, remove placeholders
        self.fields["client"].label = "Client"
        self.fields["domain"].label = "Domain"
        self.fields["host"].label = "Host"
        self.fields["package"].label = "Package"
        self.fields["status"].label = "Status"  # 👈 added

        self.fields["domain"].widget.attrs.pop("placeholder", None)
        self.fields["package"].widget.attrs.pop("placeholder", None)
