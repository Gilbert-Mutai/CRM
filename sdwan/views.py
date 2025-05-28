from django.shortcuts import render

# Create your views here.

def sdwan_records(request):
    return render(request, 'sdwan_records.html')
