from django import forms
from .models import VeeamJob
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
        choices=VeeamJob.SITE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    os = forms.ChoiceField(
        choices=VeeamJob.OS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    managed_by = forms.ChoiceField(
        choices=VeeamJob.MANAGED_BY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    job_status = forms.ChoiceField(
        choices=VeeamJob.JOB_STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    computer_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    tag = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        initial="Not set",
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )

    class Meta:
        model = VeeamJob
        fields = [
            "client",
            "site",
            "computer_name",
            "tag",
            "os",
            "managed_by",
            "job_status",
            "comment",
        ]


class AddVeeamForm(BaseVeeamForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide labels and use placeholders instead
        for field in self.fields.values():
            field.label = ""
        self.fields["computer_name"].widget.attrs["placeholder"] = "Computer Name"
        self.fields["tag"].widget.attrs["placeholder"] = "Tag (Optional)"


class UpdateVeeamForm(BaseVeeamForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show proper labels
        self.fields["client"].label = "Client"
        self.fields["site"].label = "Site"
        self.fields["computer_name"].label = "Computer Name"
        self.fields["tag"].label = "Tag"
        self.fields["os"].label = "Operating System"
        self.fields["managed_by"].label = "Managed By"
