from django import forms
from .models import Veeam
from core.models import Client


class ClientNameOnlyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class BaseVeeamForm(forms.ModelForm):
    client = ClientNameOnlyChoiceField(
        queryset=Client.objects.order_by("name"),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_client"}),
        empty_label="Select Client",
    )

    site = forms.ChoiceField(
        choices=Veeam.SITE_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    os = forms.ChoiceField(
        choices=Veeam.OS_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    managed_by = forms.ChoiceField(
        choices=Veeam.MANAGED_BY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    computer_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Veeam
        fields = [
            "client",
            "site",
            "computer_name",
            "os",
            "managed_by",
        ]


class AddVeeamForm(BaseVeeamForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide labels and use placeholders instead
        for field in self.fields.values():
            field.label = ""
        self.fields["computer_name"].widget.attrs["placeholder"] = "Computer Name"


class UpdateVeeamForm(BaseVeeamForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show proper labels
        self.fields["client"].label = "Client"
        self.fields["site"].label = "Site"
        self.fields["computer_name"].label = "Computer Name"
        self.fields["os"].label = "Operating System"
        self.fields["managed_by"].label = "Managed By"
