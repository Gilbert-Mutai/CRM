from django.shortcuts import render

# Create your views here.


def nova_records(request):
    return render(request, "nova_records.html")
