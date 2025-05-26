from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddThreeCXForm
from .models import ThreeCX

def threecx_records(request): 
    records = ThreeCX.objects.all().order_by('-last_updated', '-created_at')
    context = {'records': records}
    return render(request, 'records.html', context)


def threecx_record_details(request, pk):
    if request.user.is_authenticated:
        customer_record = get_object_or_404(ThreeCX, id=pk)
        return render(request, 'record_details.html', {'customer_record': customer_record})
    else:
        messages.warning(request, "You must be logged in to view that page.")
        return redirect('home')


def delete_threecx_record(request, pk):
    if request.user.is_authenticated:
        record_to_delete = get_object_or_404(ThreeCX, id=pk)
        record_to_delete.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('threecx_records')
    else:
        messages.warning(request, "You must be logged in to do that.")
        return redirect('login')


def add_threecx_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddThreeCXForm(request.POST)
            if form.is_valid():
                new_record = form.save(commit=False)
                new_record.created_by = request.user
                new_record.updated_by = request.user
                new_record.save()
                messages.success(request, "Record has been added!")
                return redirect('threecx_records')
        else:
            form = AddThreeCXForm()
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('login')


def update_threecx_record(request, pk):
    if request.user.is_authenticated:
        current_record = get_object_or_404(ThreeCX, id=pk)
        form = AddThreeCXForm(request.POST or None, instance=current_record)
        
        if form.is_valid():
            updated_record = form.save(commit=False)
            updated_record.updated_by = request.user
            updated_record.save()
            messages.success(request, "Record has been updated!")
            return redirect('threecx_record', pk=pk)

        return render(request, 'update_record.html', {
            'form': form,
            'customer_record': current_record 
        })
    else:
        messages.warning(request, "You must be logged in.")
        return redirect('login')

def send_notification(request):
    if request.method == "POST":
        emails = request.POST.get('emails', '').split(',')
        return render(request, 'email_notification.html', {'emails': emails})
    return redirect('threecx_records')
