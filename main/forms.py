from django import forms
from .models import Mailing

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['subject', 'body', 'send_time', 'frequency', 'status', 'clients']