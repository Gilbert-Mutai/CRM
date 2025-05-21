from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

# Create your views here.

# @login_required
def home(request):
    return render(request, 'home.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('records')  # Redirect to home after login
        else:
            messages.warning(request, "Invalid username or password. Please try again.")
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
        messages.warning(request, "You are not authorized to perform this action!")
        return redirect('records')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully added!")
            # Redirect admin to the records page after registration
            return redirect('records') 
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

@login_required
def customer_records(request):
	return render(request, 'records.html')

