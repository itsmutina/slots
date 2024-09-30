from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.html import format_html
from .models import Slot
from .forms import BulkUploadForm

class SlotAdmin(admin.ModelAdmin):
    list_display = ('link', 'is_active', 'last_checked')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name="bulk_upload")
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request):
        """Handles the form for bulk uploading slots."""
        if request.method == 'POST':
            form = BulkUploadForm(request.POST)
            if form.is_valid():
                links = form.cleaned_data['links'].splitlines()
                for link in links:
                    if link.strip():  # Check for non-empty lines
                        Slot.objects.create(link=link.strip(), is_active=True)
                self.message_user(request, "Bulk upload successful!")
                return redirect('admin:slots_slot_changelist')
        else:
            form = BulkUploadForm()

        context = {
            'form': form,
            'title': 'Bulk Upload Slot Links',
        }

        return render(request, 'admin/bulk_upload.html', context)

    def bulk_upload_button(self, request):
        """Creates a button in the admin interface for bulk uploading slots."""
        return format_html('<a class="button" href="{}">Bulk Upload</a>', '/admin/slots/slot/bulk-upload/')

    def changelist_view(self, request, extra_context=None):
        """Override the changelist view to include the bulk upload button."""
        extra_context = extra_context or {}
        extra_context['bulk_upload_button'] = self.bulk_upload_button(request)
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Slot, SlotAdmin)
