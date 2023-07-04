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

def send_mailing_task(mailing):
    """
    Логика рассылки сообщений
    """
    #mailings = Mailing.objects.filter(status='running')

    #for mailing_item in mailings:
    #    subject = mailing_item.subject
    #    message = mailing_item.body
    #    recipient_list = ['wrxwerrr@yandex.ru']
    #    send_mail(subject, message, settings.EMAIL_HOST_USER,  recipient_list=recipient_list)
    subject = mailing.subject
    message = mailing.body
    recipient_list = ['wrxwerrr@yandex.ru']
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=recipient_list)
    print("Рассылка отправлена")


def start_scheduler():
    """
    Запуск самого шедьюлера
    """
    schedule.every(25).seconds.do(check_mailings)  # Периодически проверяем рассылки
    while True:  # Запуск цикла для непрерывного выполнения задач
        schedule.run_pending()
        time.sleep(15)

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
            print('this')
            send_datetime = tz.localize(datetime.datetime.combine(send_date, send_time))
            print(send_datetime)
            if send_datetime <= current_time:
                schedule_mailing(mailing)

def schedule_mailing(mailing):
    """
    Шедьюл отправка рассылки
    """
    current_time = timezone.now()

    mailing_attempt_l = MailingAttempt.objects.filter(mailing__status='running', is_active=True)
    for mailing_attempt in mailing_attempt_l:
        print(mailing_attempt)
        if mailing_attempt and (current_time - mailing_attempt.send_datetime).total_seconds() >= 20:    # Проверяем, прошло ли подходящее время
            mailing_attempt.is_active = False  # Установка is_active предыдущей активной строки в False
            mailing_attempt.save()
            mailing_attempt = MailingAttempt.objects.create(mailing=mailing_attempt.mailing,send_datetime=timezone.now(),status='success',server_response='OK', is_active=True)
            mailing_attempt.save()
            send_mailing_task(mailing)
