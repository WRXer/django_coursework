from django.contrib import admin

from main.models import Mailing, Client, MailingAttempt


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'send_time', 'frequency', 'status', 'get_clients_display' )

    def get_clients_display(self, obj):
        return "\n".join([str(client) for client in obj.clients.all()])

    get_clients_display.short_description = 'Клиенты'


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('send_datetime', 'server_response', 'status', 'get_mailing_subject', )

    def get_mailing_subject(self, obj):
        return obj.mailing.subject if obj.mailing else None

    get_mailing_subject.short_description = 'Тема рассылки'