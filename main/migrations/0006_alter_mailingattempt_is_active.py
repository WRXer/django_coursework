# Generated by Django 4.2.2 on 2023-06-15 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_client_options_alter_mailing_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingattempt',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активная'),
        ),
    ]