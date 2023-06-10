from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Client(models.Model):
    """
    Клиент сервиса
    """
    email = models.EmailField()    #контактный email
    full_name = models.CharField(max_length=255)   #фио
    comment = models.TextField()    #комментарий

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'


class Mailing(models.Model):
    """
    Рассылка
    """
    TIME_CHOICES = (
        ('morning', 'Утро'),
        ('afternoon', 'День'),
        ('evening', 'Вечер'),
    )   #время рассылки

    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )   #периодичность: раз в день, раз в неделю, раз в месяц

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    )   #статус рассылки (завершена, создана, запущена)

    send_time = models.CharField(max_length=10, choices=TIME_CHOICES)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"Рассылка {self.id}"

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailings'


class MailingMessage(models.Model):
    """
    Сообщение для рассылки
    """
    subject = models.CharField(max_length=255)  #тема письма
    body = models.TextField()   #тело письма
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'mailing_message'
        verbose_name_plural = 'mailing_messages'


class MailingAttempt(models.Model):
    """
    Логи рассылки
    """
    STATUS_CHOICES = (
        ('success', 'Успешно'),
        ('failure', 'Ошибка'),
    )

    send_datetime = models.DateTimeField(default=timezone.now)  #дата и время последней попытки
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)    #статус попытки
    server_response = models.TextField(blank=True, null=True)   #ответ почтового сервера, если он был
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Попытка рассылки {self.id}"

    class Meta:
        verbose_name = 'mailing_attempt'