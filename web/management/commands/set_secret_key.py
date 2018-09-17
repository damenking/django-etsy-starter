from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):

    def handle(self, *args, **options):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        random_string = get_random_string(50, chars)
        f = open("django_secret_key.py","w+")
        f.write("SECRET_KEY = \'{}\'".format(random_string))
