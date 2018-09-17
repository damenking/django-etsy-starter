from django.db import models


class EtsyUser(models.Model):
    etsy_user_id = models.IntegerField(unique=True)
    login_name = models.CharField(max_length=200)


class Shop(models.Model):
    shop_id = models.IntegerField(unique=True)
    shop_name = models.CharField(max_length=200)
    title = models.CharField(null=True, max_length=500)
    announcement = models.CharField(null=True, max_length=500)
    image_url_760x100 = models.CharField(null=True, max_length=200)
    icon_url_fullxfull = models.CharField(null=True, max_length=200)
    last_updated_tsz = models.DateTimeField()
    deleted = models.BooleanField(default=False)
    etsy_user = models.ForeignKey(
        EtsyUser,
        on_delete=models.SET_NULL,
        null=True
    )


class Listing(models.Model):
    listing_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    last_modified_tsz = models.DateTimeField()
    deleted = models.BooleanField(default=False)
    main_image = models.ForeignKey(
        'ListingImage',
        on_delete=models.SET_NULL,
        null=True,
        related_name='main_image_listing'
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        null=True,
        related_name='listings'
    )


class ListingImage(models.Model):
    listing_image_id = models.IntegerField(unique=True)
    rank = models.IntegerField()
    url_75x75 = models.CharField(max_length=200, null=True)
    url_170x135 = models.CharField(max_length=200, null=True)
    url_570xN = models.CharField(max_length=200, null=True)
    url_fullxfull = models.CharField(max_length=200)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.SET_NULL,
        null=True,
        related_name='listing_images'
    )
