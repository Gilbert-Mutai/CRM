from django.shortcuts import render

# Create your views here.

def pm_records(request):
    return render(request, 'pm_records.html')
