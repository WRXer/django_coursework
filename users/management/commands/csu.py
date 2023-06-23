from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='wrxwerrr@yandex.ru',
            first_name='Admin',
            last_name='Wrxwerrr',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password('12345qwerty')
        user.save()