from django import forms
from .models import Mailing, Client, MailingAttempt


class MailingForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(queryset=Client.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Mailing
        fields = ['subject', 'body', 'send_time', 'frequency', 'clients', 'status']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']


class MailingAttemptForm(forms.ModelForm):
    class Meta:
        model=MailingAttempt
        fields = '__all__'