from django import forms
from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Issue with item quality'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please describe the issue in detail...'}),
        }
