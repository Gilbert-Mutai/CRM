from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm
from .forms import SignUpForm
from django.utils.crypto import get_random_string

User = get_user_model()


# Existing views

def home(request):
    return render(request, 'home.html')


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('records')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.warning(request, "You have been logged out!")
    return redirect('home')


@login_required
def register_user(request):
    # Restrict access to admin users only
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to perform this action!")
        return redirect('records')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Instead of just form.save(), we'll create the user with inactive status and send email
            email = form.cleaned_data.get('email')

            # Create user with a temporary password and inactive status
            temp_password = get_random_string(10)
            user = User.objects.create_user(email=email, password=temp_password)
            user.is_active = False
            user.save()

            # Send email with password setup link
            send_confirmation_email(user)

            messages.success(request, "User added successfully!")
            return redirect('records')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


@login_required
def customer_records(request):
    return render(request, 'records.html')


# --- New functions for email confirmation flow ---

def send_confirmation_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = f"http://localhost:8000{reverse('set_new_password', kwargs={'uidb64': uid, 'token': token})}"

    send_mail(
        subject="Welcome to Angani CRM - Set your New Password",
        message=f"Hello, please click the link below to set your password:\n{link}",
        from_email = "Angani CRM <gmutai1194@gmail.com>",
        recipient_list=[user.email],
    )



def set_new_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                user.is_active = True
                user.save()
                messages.success(request, "Password set successfully!")
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'set_password.html', {'form': form})
    else:
        return render(request, 'invalid_link.html')
