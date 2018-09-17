from rest_framework import viewsets

from etsy.models import Listing
from etsy.serializers import ListingsSerializer


class ListingsViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.filter(deleted=False)
    serializer_class = ListingsSerializer
