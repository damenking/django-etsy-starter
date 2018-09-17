from rest_framework import serializers

from etsy.models import Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListingImage
        fields = '__all__'


class ListingsSerializer(serializers.ModelSerializer):

    listing_images = ListingImageSerializer(many=True)
    main_image = ListingImageSerializer()
    
    class Meta:
        model = Listing
        fields = '__all__'