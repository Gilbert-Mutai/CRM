from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('3cx/', include('threecx.urls')),
    path('domain/', include('domains.urls')),
    path('nova/', include('nova.urls')),
    path('novapool4/', include('novapool4.urls')), 
    path('sd-wan/', include('sdwan.urls')),
    path('cloudberry/', include('cloudberry.urls')),
    path('veeam/', include('veeam.urls')),
    path('project-manager/', include('pm.urls')),
]
