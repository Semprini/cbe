"""cbe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import cbe.party.views as PartyViews
import cbe.location.views as LocationViews
#import cbe.business_interaction.views as BusinessInteractionViews
import cbe.customer.views as CustomerViews
import cbe.trouble.views as TroubleViews
import cbe.physical_object.views as PhysicalObjectViews
import cbe.supplier_partner.views as SupplierPartnerViews


admin.site.site_title = 'CBE'
admin.site.site_header = 'Common Business Entities'

# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ContentType
        fields = ('url', 'app_label', 'model', 'name', )

# ViewSets define the view behavior.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

cberouter = DefaultRouter()
cberouter.register(r'party/individual', PartyViews.IndividualViewSet)
cberouter.register(r'party/organisation', PartyViews.OrganisationViewSet)
cberouter.register(
    r'party/generic_party_role', PartyViews.GenericPartyRoleViewSet)
cberouter.register(
    r'party/telephone_number', PartyViews.TelephoneNumberViewSet)

cberouter.register(r'location/country', LocationViews.CountryViewSet)
cberouter.register(r'location/city', LocationViews.CityViewSet)
cberouter.register(
    r'location/urban_property_address', LocationViews.UrbanPropertyAddressViewSet)
cberouter.register(
    r'location/po_box_address', LocationViews.PoBoxAddressViewSet)
cberouter.register(
    r'location/absolute_local_location', LocationViews.AbsoluteLocalLocationViewSet)

# cberouter.register(r'business_interaction/business_interaction',
                   # BusinessInteractionViews.BusinessInteractionViewSet)
# cberouter.register(r'business_interaction/business_interaction_item',
                   # BusinessInteractionViews.BusinessInteractionItemViewSet)

cberouter.register(r'customer/customer', CustomerViews.CustomerViewSet)
cberouter.register(r'customer/account', CustomerViews.CustomerAccountViewSet)
cberouter.register(r'customer/customer_account_contact',
                   CustomerViews.CustomerAccountContactViewSet)

cberouter.register(r'trouble/problem', TroubleViews.ProblemViewSet)

cberouter.register(r'physical_object/structure', PhysicalObjectViews.StructureViewSet)
cberouter.register(r'physical_object/vehicle', PhysicalObjectViews.VehicleViewSet)
cberouter.register(r'physical_object/device', PhysicalObjectViews.DeviceViewSet)

cberouter.register(r'supplier_partner/supplier', SupplierPartnerViews.SupplierViewSet)
cberouter.register(r'supplier_partner/partner', SupplierPartnerViews.PartnerViewSet)
cberouter.register(r'supplier_partner/buyer', SupplierPartnerViews.BuyerViewSet)

router = DefaultRouter()
router.register(r'auth/users', UserViewSet)
router.register(r'content_types', ContentTypeViewSet)

for route in cberouter.registry:
    router.register(route[0], route[1])

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
]
