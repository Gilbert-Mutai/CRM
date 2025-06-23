from django.shortcuts import render

# Create your views here.


def cloudberry_records(request):
    return render(request, "cloudberry_records.html")
