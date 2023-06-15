from django.conf import settings
from django.core.mail import send_mail
from main.models import Mailing
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
    last_sent_time = None
    mailings = Mailing.objects.all()  # Получаем все рассылки
    for mailing in mailings:
        if mailing.status == 'running':
            schedule_mailing(mailing, last_sent_time)

def schedule_mailing(mailing, last_sent_time):
    """
    Шедьюл отправка рассылки
    """
    current_time = datetime.datetime.now()
    if last_sent_time is None or (current_time - last_sent_time).total_seconds() >= 10:  # Проверяем, прошло ли подходящее время
        send_mailing_task()
        last_sent_time = current_time
        print("Рассылка отправлена")


