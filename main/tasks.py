import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
import pytz
from main.models import Mailing, MailingAttempt
import datetime
import threading
import time
import schedule


last_sent_time = None



def start_scheduler():
    """
    Запуск самого шедьюлера
    """
    print('ну шо Поихали')
    schedule.every(25).seconds.do(check_mailings)  # Периодически проверяем рассылки
    while True:  # Запуск цикла для непрерывного выполнения задач
        schedule.run_pending()
        time.sleep(5)

def check_mailings():
    """
    Проверка статуса рассылки
    """
    tz = pytz.timezone('Europe/Moscow')
    mailings = Mailing.objects.all()  # Получаем все рассылки
    current_time = timezone.now()

    for mailing in mailings:
        if mailing.status == 'running':
            #schedule_mailing(mailing)
            send_date = mailing.send_date
            if mailing.send_time in ['Утро', 'morning']:
                send_time = datetime.time(9, 0)
            elif mailing.send_time in ['День', 'afternoon']:
                send_time = datetime.time(14, 0)
            else:
                send_time = datetime.time(19, 0)
            send_datetime = tz.localize(datetime.datetime.combine(send_date, send_time))
            print(send_datetime)
            if send_datetime <= current_time:
                send_mailing_task(mailing)

def send_mailing_task(mailing):
    """
    Логика рассылки сообщений
    """
    #mailings = Mailing.objects.filter(status='running')
    subject = mailing.subject
    message = mailing.body
    recipients = mailing.clients.all().values_list('email', flat=True)  # Получаем список email-адресов получателей
    recipient_list = list(recipients)  #['wrxwerrr@yandex.ru']
    success = True  # Флаг успешной отправки
    bad_err = None
    for recipient in recipient_list:
        print(recipient)
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=[recipient])
        except smtplib.SMTPException as error:
            bad_err = error
            success = False
    if success:
        mailing_attempt = MailingAttempt.objects.create(mailing=mailing, send_datetime=timezone.now(),
                                                        status='success', server_response='OK', is_active=True)
        mailing_attempt.save()
        print("Рассылка отправлена")
    else:
        mailing_attempt = MailingAttempt.objects.create(mailing=mailing, send_datetime=timezone.now(),
                                                        status='failure', server_response=bad_err, is_active=False)
        mailing_attempt.save()
        print(f"Ошибка при отправке рассылки.")
