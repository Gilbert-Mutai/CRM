from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from .models import CustomUser,ThreeCX

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    password1 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text=""
    )
    password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        help_text=""
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        
    

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )


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
    licence_type = forms.ChoiceField(
        choices=ThreeCX.LICENCE_TYPES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=""
    )

    class Meta:
        model = ThreeCX
        exclude = ('created_by', 'updated_by')
