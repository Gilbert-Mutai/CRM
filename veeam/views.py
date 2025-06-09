from django.shortcuts import render

# Create your views here.

def veeam_records(request):
    return render(request, 'veeam_records.html')
