# Generated by Django 4.2.2 on 2023-07-03 10:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blogpost_options_alter_blogpost_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='активно'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='pub_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата публикации'),
        ),
    ]