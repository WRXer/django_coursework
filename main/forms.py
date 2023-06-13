from django import forms
from .models import Mailing, Client


class MailingForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(queryset=Client.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Mailing
        fields = ['subject', 'body', 'send_time', 'frequency', 'status', 'clients']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']
