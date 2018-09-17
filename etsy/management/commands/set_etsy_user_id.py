import json
import requests
from django.core.management.base import BaseCommand
from django.conf import settings


base_url = settings.ETSY_BASE_URL
key = settings.ETSY_API_KEY


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--shop_name')

    def handle(self, *args, **options):
        shop_name = options['shop_name']
        url = base_url + '/shops/{}?api_key={}'.format(shop_name, key)
        response = requests.request("GET", url)
        data = response.json()
        user_id = data['results'][0]['user_id']
        f = open("etsy_user_id.py","w+")
        f.write("ETSY_USER_ID = {}".format(user_id))
