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
            #send_datetimee = datetime.combine(send_date, send_time)
            send_datetimee = datetime.datetime(year=send_date.year,month=send_date.month,day=send_date.day,hour=send_time.hour,minute=send_time.minute,second=send_time.second, )
            current_time = current_time.replace(tzinfo=None)
            send_datetimee = send_datetimee.replace(tzinfo=None)
            if send_datetimee <= current_time:
                last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-send_datetime').first()
                last_attempt_date = last_attempt.send_datetime if last_attempt else None
                frequency = mailing.frequency
                if should_reschedule_mailing(last_attempt_date, send_time, frequency,current_time):
                    send_mailing_task(mailing)

def should_reschedule_mailing(last_attempt_date, send_time, frequency,current_time):
    """
    Проверка рассылки на условие интервала времени
    """
    send_date = datetime.datetime(year=last_attempt_date.year, month=last_attempt_date.month, day=last_attempt_date.day, hour=send_time.hour, minute=send_time.minute,)
    if send_date is None:
        return True
    elif frequency == 'daily':
        return send_date.date() < current_time.date()
    elif frequency == 'weekly':
        return send_date.date() + timedelta(days=7) <= current_time.date()
    if frequency == 'monthly':
        return send_date.date() + timedelta(days=30) <= current_time.date()
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
    if success:    #Если отправка верна, то
        mailing_attempt = MailingAttempt.objects.create(mailing=mailing, send_datetime=timezone.now(),
                                                        status='success', server_response='OK', is_active=True)
        mailing_attempt.save()
        print("Рассылка отправлена")
    else:
        mailing_attempt = MailingAttempt.objects.create(mailing=mailing, send_datetime=timezone.now(),
                                                        status='failure', server_response=bad_err, is_active=False)
        mailing_attempt.save()
        print(f"Ошибка при отправке рассылки.")
