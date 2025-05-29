# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .forms import SignUpForm
from .utils import authenticate_user, create_inactive_user, send_confirmation_email
from django.contrib.auth import get_user_model

User = get_user_model()

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate_user(email, password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('menu')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.warning(request, "You have been logged out!")
    return redirect('login')


@login_required
def register_user(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to perform this action!")
        return redirect('login')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            user, temp_password = create_inactive_user(email, first_name, last_name)
            send_confirmation_email(user)

            messages.success(request, "User added successfully!")
            return redirect('menu')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


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
