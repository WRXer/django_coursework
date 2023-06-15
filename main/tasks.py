from django.conf import settings
from django.core.mail import send_mail
from main.models import Mailing
import time
import schedule
from datetime import datetime



def send_mailing_task():
    """
    Логика рассылки сообщений
    """
    mailings = Mailing.objects.filter(status='running')

    for mailing_item in mailings:
        subject = mailing_item.subject
        message = mailing_item.body
        recipient_list = ['wrxwerrr@yandex.ru']
        send_mail(subject, message, settings.EMAIL_HOST_USER,  recipient_list=recipient_list)
    #subject = 'Test'
    #message = 'test'
    #recipient_list = ['wrxwerrr@yandex.ru']
    #send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=recipient_list)
    print('Отправлено')

        #send_mail(        'Рассылочка'        f'{mailing_item.subject}',        settings.EMAIL_HOST_USER,        recipient_list = ['king_311@mail.ru']    )


