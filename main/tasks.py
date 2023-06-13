from django.conf import settings
from django.core.mail import send_mail
from django_cron import CronJobBase, Schedule
from main.models import Mailing
import time


def send_mailing_task(mailing_item: Mailing):
    """
    Логика рассылки сообщений

    mailings = Mailing.objects.filter(status='running')

    for mailing_item in mailings:
        recipients = mailing_item.recipients.all()
        subject = mailing_item.subject
        message = mailing_item.body
        recipient_list = ['wrxwerrr@yandex.ru']
        send_mail(subject, message, settings.EMAIL_HOST_USER,  recipient_list=recipient_list)"""
    subject = 'Test'
    message = 'test'
    recipient_list = ['wrxwerrr@yandex.ru']
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=recipient_list)

        #send_mail(        'Рассылочка'        f'{mailing_item.subject}',        settings.EMAIL_HOST_USER,        recipient_list = ['king_311@mail.ru']    )




class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 0.167  # Запускать каждый minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main.my_cron_job'  # Путь к вашей задаче

    def do(self):
        # Ваш код для выполнения периодической задачи
        print('contact')
        subject = 'Test'
        message = 'test'
        recipient_list = ['wrxwerrr@yandex.ru']
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=recipient_list)

