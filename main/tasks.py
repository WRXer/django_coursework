from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from main.models import Mailing, MailingAttempt
import datetime
import threading
import time
import schedule


last_sent_time = None

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
    print("Рассылка отправлена")


def start_scheduler():
    """
    Запуск самого шедьюлера
    """
    schedule.every(10).seconds.do(check_mailings)  # Периодически проверяем рассылки
    while True:  # Запуск цикла для непрерывного выполнения задач
        schedule.run_pending()
        time.sleep(5)

def check_mailings():
    """
    Проверка статуса рассылки
    """
    mailings = Mailing.objects.all()  # Получаем все рассылки
    for mailing in mailings:
        if mailing.status == 'running':
            schedule_mailing(mailing)

def schedule_mailing(mailing):
    """
    Шедьюл отправка рассылки
    """
    current_time = timezone.now()
    mailing = Mailing.objects.first()  # Получаем рассылку
    mailing_attempt = MailingAttempt.objects.filter(mailing__status='running', is_active=True).first()

    if mailing_attempt and (current_time - mailing_attempt.send_datetime).total_seconds() >= 20:    # Проверяем, прошло ли подходящее время
        mailing_attempt.is_active = False  # Установка is_active предыдущей активной строки в False
        mailing_attempt.save()
        mailing_attempt = MailingAttempt.objects.create(mailing=mailing,send_datetime=timezone.now(),status='success',server_response='OK', is_active=True)
        mailing_attempt.save()
        send_mailing_task()
