import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import pytz
from main.models import Mailing, MailingAttempt
import datetime
import time
import schedule
from datetime import timedelta



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
            send_date = mailing.send_date
            if mailing.send_time in ['Утро', 'morning']:
                send_time = datetime.time(9, 0)
            elif mailing.send_time in ['День', 'afternoon']:
                send_time = datetime.time(14, 0)
            else:
                send_time = datetime.time(19, 0)
            send_datetimee = tz.localize(datetime.datetime.combine(send_date, send_time))
            print(send_datetimee)
            if send_datetimee <= current_time:
                last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-send_datetime').first()
                last_attempt_date = last_attempt.send_datetime if last_attempt else None
                frequency = mailing.frequency
                if should_reschedule_mailing(last_attempt_date, frequency,current_time):
                    print('check heck')
                    send_mailing_task(mailing)

def should_reschedule_mailing(last_attempt_date, frequency,current_time):
    if last_attempt_date is None:
        return True
    elif frequency == 'daily':
        return last_attempt_date.date() < current_time.date()

    elif frequency == 'weekly':
        return last_attempt_date.date() + timedelta(days=7) <= current_time.date()

    if frequency == 'monthly':
        return last_attempt_date.date() + timedelta(days=30) <= current_time.date()
    return False  # Некорректная периодичность

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
