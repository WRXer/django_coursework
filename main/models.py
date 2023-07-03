from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class Client(models.Model):
    """
    Клиент сервиса
    """
    email = models.EmailField(verbose_name='емейл')    #контактный email
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')   #фио
    comment = models.TextField(verbose_name='Комментарий')    #комментарий

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('main:client_detail', kwargs={'pk': self.pk})


    class Meta:
        ordering = ['id']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


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

    subject = models.CharField(max_length=255, verbose_name='Тема письма')  # тема письма
    body = models.TextField(verbose_name= "Тело письма")  # тело письма
    send_time = models.CharField(max_length=10, choices=TIME_CHOICES, verbose_name="Время отправки")
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='Частота отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    mailing_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"Рассылка {self.id}"

    def get_absolute_url(self):
        return reverse('main:mailing_detail', kwargs={'pk': self.pk})


    class Meta:
        ordering = ['id']
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):
    """
    Логи рассылки
    """
    STATUS_CHOICES = (
        ('success', 'Успешно'),
        ('failure', 'Ошибка'),
    )

    send_datetime = models.DateTimeField(default=timezone.now, verbose_name='Последняя попытка')  #дата и время последней попытки
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус попытки')    #статус попытки
    server_response = models.TextField(blank=True, null=True, verbose_name='Ответ сервера')   #ответ почтового сервера, если он был
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Активная')

    def __str__(self):
        return f"Попытка рассылки {self.id}"

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Лог рассылки'
