# Generated by Django 4.2.2 on 2023-06-12 15:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Тема письма')),
                ('body', models.TextField(verbose_name='Тело письма')),
                ('send_time', models.CharField(choices=[('morning', 'Утро'), ('afternoon', 'День'), ('evening', 'Вечер')], max_length=10, verbose_name='Время отправки')),
                ('frequency', models.CharField(choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=10, verbose_name='Частота отправки')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('running', 'Запущена'), ('completed', 'Завершена')], max_length=10, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterField(
            model_name='client',
            name='comment',
            field=models.TextField(verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='емейл'),
        ),
        migrations.AlterField(
            model_name='client',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='Полное имя'),
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Последняя попытка')),
                ('status', models.CharField(choices=[('success', 'Успешно'), ('failure', 'Ошибка')], max_length=10, verbose_name='Статус попытки')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='Ответ сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mailing')),
            ],
            options={
                'verbose_name': 'Лог рассылки',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='clients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client'),
        ),
    ]
