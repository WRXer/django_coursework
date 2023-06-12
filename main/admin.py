from django.contrib import admin

from main.models import Mailing, Client


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'send_time', 'frequency', 'status', 'get_client_name', )

    def get_client_name(self, obj):
        return obj.clients.full_name if obj.clients else None

    get_client_name.short_description = 'Имя клиента'