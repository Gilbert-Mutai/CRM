from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
def menu(request):
    return render(request, 'menu.html')

