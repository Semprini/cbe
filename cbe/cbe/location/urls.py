"""cbe location URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

import cbe.location.views as LocationViews

router = AppRouter(root_view_name='app-location')
router.register(r'geographic_area', LocationViews.GeographicAreaViewSet)
router.register(r'country', LocationViews.CountryViewSet)
router.register(r'city', LocationViews.CityViewSet)
router.register(r'urban_property_address', LocationViews.UrbanPropertyAddressViewSet)
router.register(r'po_box_address', LocationViews.PoBoxAddressViewSet)
router.register(r'location', LocationViews.LocationViewSet)

urlpatterns = [
    url(r'^api/location/', include(router.urls)),
]
