from django.shortcuts import render
from .models import Slot
import requests

def check_slot_status(slot):
    """Check if the slot link is active or not."""
    try:
        response = requests.get(slot.link)
        if response.status_code == 404:
            slot.is_active = False
            slot.save()
    except requests.RequestException:
        # Handle connection issues or other exceptions
        slot.is_active = False
        slot.save()

def slot_list(request):
    """View to list all active slots and check their status."""
    slots = Slot.objects.filter(is_active=True)
    total_links = Slot.objects.count()
    
    # Check status of each slot and remove inactive ones
    for slot in slots:
        check_slot_status(slot)
    
    active_slots = Slot.objects.filter(is_active=True)
    return render(request, 'slots/slot_list.html', {'slots': active_slots, 'total_links': total_links})


def inactive_slots(request):
    """View to list all inactive slots."""
    inactive_slots = Slot.objects.filter(is_active=False)
    return render(request, 'slots/inactive_slots.html', {'inactive_slots': inactive_slots})
def bulk_upload_view(self, request):
    """Handle the bulk upload form and silently skip duplicate links."""
    if request.method == 'POST':
        form = BulkUploadForm(request.POST)
        if form.is_valid():
            links = form.cleaned_data['links'].splitlines()
            duplicates_skipped = 0
            new_links_added = 0
            for link in links:
                clean_link = link.strip()
                if clean_link:  # Check for non-empty lines
                    # Check if the link already exists in the database
                    if Slot.objects.filter(link=clean_link).exists():
                        duplicates_skipped += 1  # Increment duplicate count
                    else:
                        Slot.objects.create(link=clean_link, is_active=True)
                        new_links_added += 1  # Increment new links count

            # Display a message with the number of new links and duplicates skipped
            self.message_user(request, f"Bulk upload successful! {new_links_added} new links added, {duplicates_skipped} duplicates skipped.")
            return redirect('admin:slots_slot_changelist')
    else:
        form = BulkUploadForm()

    context = {
        'form': form,
        'title': 'Bulk Upload Slot Links',
    }

    return render(request, 'admin/bulk_upload.html', context)
