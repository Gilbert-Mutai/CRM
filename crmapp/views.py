from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm
from .forms import SignUpForm,AddThreeCXForm
from django.utils.crypto import get_random_string
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import ThreeCX


User = get_user_model()


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
            return redirect('threecx_records')
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
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to perform this action!")
        return redirect('threecx_records')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            temp_password = get_random_string(10)

            user = User.objects.create_user(
                email=email,
                password=temp_password,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = False
            user.save()

            send_confirmation_email(user)

            messages.success(request, "User added successfully!")
            return redirect('records')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def send_confirmation_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = f"http://localhost:8000{reverse('set_new_password', kwargs={'uidb64': uid, 'token': token})}"

    context = {
        'user_name': user.get_short_name(),
        'cta_link': link,
        'current_year': datetime.now().year,
    }

    subject = "Welcome to Angani Client Manager - Set your New Password"
    from_email = "Angani Client Manager <noreply.anganicrm@gmail.com>"
    to_email = [user.email]
    text_content = f"Hello {context['user_name']},\n\nPlease click the link below to set your password:\n{link}\n\nAngani CRM Team"
    html_content = render_to_string("welcome_email.html", context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
    

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
    

def threecx_records(request): 
    records = ThreeCX.objects.all().order_by('-last_updated', '-created_at')
    context = {'records': records}
    return render(request, 'records.html', context)


def threecx_record_details(request, pk):
    if request.user.is_authenticated:
        customer_record = get_object_or_404(ThreeCX, id=pk)
        return render(request, 'record_details.html', {'customer_record': customer_record})
    else:
        messages.warning(request, "You must be logged in to view that page.")
        return redirect('home')


def delete_threecx_record(request, pk):
    if request.user.is_authenticated:
        record_to_delete = get_object_or_404(ThreeCX, id=pk)
        record_to_delete.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('threecx_records')
    else:
        messages.warning(request, "You must be logged in to do that.")
        return redirect('login')


def add_threecx_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddThreeCXForm(request.POST)
            if form.is_valid():
                new_record = form.save(commit=False)
                new_record.created_by = request.user
                new_record.updated_by = request.user
                new_record.save()
                messages.success(request, "Record has been added!")
                return redirect('threecx_records')
        else:
            form = AddThreeCXForm()
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('login')


def update_threecx_record(request, pk):
    if request.user.is_authenticated:
        current_record = get_object_or_404(ThreeCX, id=pk)
        form = AddThreeCXForm(request.POST or None, instance=current_record)
        
        if form.is_valid():
            updated_record = form.save(commit=False)
            updated_record.updated_by = request.user
            updated_record.save()
            messages.success(request, "Record has been updated!")
            return redirect('threecx_record', pk=pk)

        return render(request, 'update_record.html', {
            'form': form,
            'customer_record': current_record 
        })
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('login')

def compose_email(request):
    if request.method == "POST":
        emails = request.POST.get('emails', '').split(',')
        return render(request, 'compose_email.html', {'emails': emails})
    return redirect('threecx_records')
