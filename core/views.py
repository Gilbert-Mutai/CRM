from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
def menu(request):
    client_sections = [
        {"title": "3CX Clients", "url_name": "threecx_records", "icon": "telephone", "btn_class": "primary"},
        {"title": "Domain & Hosting", "url_name": "domain_records", "icon": "globe", "btn_class": "success"},
        {"title": "Nova Clients", "url_name": "nova_records", "icon": "lightning-charge", "btn_class": "warning"},
        {"title": "Novapool 4 Clients", "url_name": "novapool4_records", "icon": "cpu", "btn_class": "warning"},
        {"title": "SD-WAN Clients", "url_name": "sdwan_records", "icon": "diagram-3", "btn_class": "primary"},
        {"title": "Project Manager", "url_name": "pm_records", "icon": "kanban", "btn_class": "info"},
    ]
    return render(request, 'menu.html', {'client_sections': client_sections})
