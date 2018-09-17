import json
import requests
import pytz
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from etsy.models import EtsyUser, Shop, Listing, ListingImage

base_url = settings.ETSY_BASE_URL
key = settings.ETSY_API_KEY
user_id = settings.ETSY_USER_ID


class Command(BaseCommand):
    # This could all probably be optimized but the data volume should be small
    # so probably no big deal.
    listing_set = set()
    shop_set = set()

    def handle(self, *args, **options):
        self.update_etsy_user()
        self.update_shops()
        self.update_listings()
        self.update_images()

    def update_etsy_user(self):
        url = base_url + '/users/{}/?api_key={}'.format(user_id, key)
        response = requests.request("GET", url)
        data = response.json()
        results = data['results'][0]
        try:
            etsy_user = EtsyUser.objects.get(etsy_user_id=user_id)
            etsy_user.login_name=results['login_name']
            etsy_user.save()
        except:
            new_user = EtsyUser(
                etsy_user_id=user_id,
                login_name=results['login_name']
            )
            new_user.save()
        
    def update_shops(self):
        url = base_url + '/users/{}/shops/?api_key={}'.format(user_id, key)
        response = requests.request("GET", url)
        data = response.json()
        results = data['results']
        for result in results:
            last_updated = datetime.fromtimestamp(result['last_updated_tsz'], pytz.UTC)
            try:
                shop = Shop.objects.get(shop_id=result['shop_id'])
                if not shop.last_updated_tsz or last_updated > shop.last_updated_tsz:
                    shop.shop_name = result['shop_name']
                    shop.title = result['title']
                    shop.announcement = result['announcement']
                    shop.image_url_760x100 = result['image_url_760x100']
                    shop.icon_url_fullxfull = result['icon_url_fullxfull']
                    shop.last_updated_tsz = last_updated
                    shop.deleted = False
                    shop.etsy_user = EtsyUser.objects.get(etsy_user_id=user_id)
                    shop.save()
            except:
                new_shop = Shop(
                    shop_id = result['shop_id'],
                    shop_name = result['shop_name'],
                    title = result['title'],
                    announcement = result['announcement'],
                    image_url_760x100 = result['image_url_760x100'],
                    icon_url_fullxfull = result['icon_url_fullxfull'],
                    last_updated_tsz = last_updated,
                    etsy_user = EtsyUser.objects.get(etsy_user_id=user_id)
                )
                new_shop.save()
            self.shop_set.add(result['shop_id'])
        shops = Shop.objects.filter(deleted=False)
        for shop in shops:
            if shop.shop_id not in self.shop_set:
                shop.deleted = True
                shop.save()
        
    def update_listings(self):
        for shop_id in self.shop_set:
            page = 1
            while True:
                url = base_url + '/shops/{}/listings/active/?limit=100&page={}&api_key={}'.format(shop_id, page, key)
                response = requests.request("GET", url)
                data = response.json()
                results = data['results']
                if not results:
                    break
                for result in results:
                    self.listing_set.add(result['listing_id'])
                    last_updated = datetime.fromtimestamp(result['last_modified_tsz'], pytz.UTC)
                    try:
                        listing = Listing.objects.get(listing_id=result['listing_id'])
                        if last_updated > listing.last_modified_tsz:
                            listing.title = result['title']
                            listing.description = result['description']
                            listing.price = result['price']
                            listing.last_modified_tsz = last_updated
                            listing.deleted = False
                            listing.shop = Shop.objects.get(shop_id=shop_id)
                            listing.save()
                    except:
                        new_listing = Listing(
                            listing_id = result['listing_id'],
                            title = result['title'],
                            description = result['description'],
                            price = result['price'],
                            last_modified_tsz = last_updated,
                            shop = Shop.objects.get(shop_id=shop_id)
                        )
                        new_listing.save()
                        self.listing_set.add(new_listing.listing_id)
                page += 1
        listings_queryset = Listing.objects.filter(deleted=False)
        for listing in listings_queryset:
            if listing.listing_id not in self.listing_set:
                listing.deleted = True
                listing.save()

    def update_images(self):
        listings = Listing.objects.all()
        for listing in listings:
            url = base_url + '/listings/{}/images?api_key={}'.format(listing.listing_id, key)
            response = requests.request("GET", url)
            data = response.json()
            results = data['results']
            for result in results:
                try:
                    ListingImage.objects.get(listing_image_id=result['listing_image_id'])
                except:
                    new_listing_image = ListingImage(
                        listing_image_id = result['listing_image_id'],
                        rank = result['rank'],
                        url_75x75 = result['url_75x75'],
                        url_170x135 = result['url_170x135'],
                        url_570xN = result['url_570xN'],
                        url_fullxfull = result['url_fullxfull'],
                        listing = listing
                    )
                    new_listing_image.save()
                if result['rank'] == 1:
                    main_image = ListingImage.objects.get(listing_image_id=result['listing_image_id'])
                    if listing.main_image != main_image:
                        listing.main_image = main_image
                        listing.save()
