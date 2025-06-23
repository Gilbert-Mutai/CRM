from django.shortcuts import render

# Create your views here.


def domain_records(request):
    return render(request, "domain_records.html")
