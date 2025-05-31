from django import forms
from .models import Client

class AddClientForm(forms.ModelForm):
    client_type = forms.ChoiceField(
        choices=Client.CLIENT_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Full Name or Company", "class": "form-control"}),
        label=""
    )
    contact_person = forms.CharField(
        required=False,  # Conditionally required if client_type is 'company'
        widget=forms.TextInput(attrs={"placeholder": "Contact Person (for Company)", "class": "form-control"}),
        label=""
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email Address", "class": "form-control"}),
        label=""
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Phone Number", "class": "form-control"}),
        label=""
    )

    class Meta:
        model = Client
        fields = ['client_type', 'name', 'contact_person', 'email', 'phone_number']
        

class ClientUpdateForm(forms.ModelForm):
    client_type = forms.ChoiceField(
        choices=Client.CLIENT_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Full Name or Company", "class": "form-control"}),
        label=""
    )
    contact_person = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={"placeholder": "Contact Person (for Company)", "class": "form-control"}),
        label=""
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email Address", "class": "form-control"}),
        label=""
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Phone Number", "class": "form-control"}),
        label=""
    )

    class Meta:
        model = Client
        fields = ['client_type', 'name', 'contact_person', 'email', 'phone_number']