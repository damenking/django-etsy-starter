from django.urls import path, include
from rest_framework.routers import DefaultRouter

from etsy.views import ListingsViewSet


router = DefaultRouter()

router.register(r'listings', ListingsViewSet, base_name='listings')

urlpatterns = [
    path('', include(router.urls))
]
