from django import forms

class BulkUploadForm(forms.Form):
    links = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter each link on a new line'}),
        label="Bulk Upload Links",
        help_text="Enter one link per line."
    )
