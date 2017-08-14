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

from cbe.routers import AppRouter
from . import views

import cbe.party.views as PartyViews
import cbe.location.views as LocationViews
#import cbe.business_interaction.views as BusinessInteractionViews
import cbe.customer.views as CustomerViews
import cbe.trouble.views as TroubleViews
import cbe.physical_object.views as PhysicalObjectViews
import cbe.supplier_partner.views as SupplierPartnerViews
import cbe.human_resources.views as HumanResourcesViews
import cbe.resource.views as ResourceViews
import cbe.information_technology.views as ITViews
import cbe.project.views as ProjectViews
import cbe.credit.views as CreditViews


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

cberouter = AppRouter()

partyrouter = AppRouter(root_view_name='app-party')
partyrouter.register(r'individual', PartyViews.IndividualViewSet)
partyrouter.register(r'organisation', PartyViews.OrganisationViewSet)
partyrouter.register(
    r'generic_party_role', PartyViews.GenericPartyRoleViewSet)
partyrouter.register(
    r'telephone_number', PartyViews.TelephoneNumberViewSet)
partyrouter.register(r'owner', PartyViews.OwnerViewSet)
partyrouter.register(r'party_role_association', PartyViews.PartyRoleAssociationViewSet)

locationrouter = AppRouter(root_view_name='app-location')
locationrouter.register(r'country', LocationViews.CountryViewSet)
locationrouter.register(r'city', LocationViews.CityViewSet)
locationrouter.register(
    r'urban_property_address', LocationViews.UrbanPropertyAddressViewSet)
locationrouter.register(
    r'po_box_address', LocationViews.PoBoxAddressViewSet)
locationrouter.register(
    r'location', LocationViews.LocationViewSet)

humanresourcesrouter = AppRouter(root_view_name='app-human_resources')
humanresourcesrouter.register(r'staff', HumanResourcesViews.StaffViewSet)
humanresourcesrouter.register(r'identification', HumanResourcesViews.IdentificationViewSet)
humanresourcesrouter.register(r'identification_type', HumanResourcesViews.IdentificationTypeViewSet)

physicalresourcerouter = AppRouter(root_view_name='app-physical_resource')
physicalresourcerouter.register(r'physical_resource', ResourceViews.PhysicalResourceViewSet)


customerrouter = AppRouter(root_view_name='app-customer')
customerrouter.register(r'customer', CustomerViews.CustomerViewSet, base_name='customer')
customerrouter.register(r'account', CustomerViews.CustomerAccountViewSet)
customerrouter.register(r'customer_account_contact',
                   CustomerViews.CustomerAccountContactViewSet)

creditrouter = AppRouter(root_view_name='app-credit')
creditrouter.register(r'credit', CreditViews.CreditViewSet)
creditrouter.register(r'credit_balance_event', CreditViews.CreditBalanceEventViewSet)
creditrouter.register(r'credit_profile', CreditViews.CreditProfileViewSet)
      
troublerouter = AppRouter(root_view_name='app-trouble')
troublerouter.register(r'problem', TroubleViews.ProblemViewSet)

physicalobjectrouter = AppRouter(root_view_name='app-physical_object')
physicalobjectrouter.register(r'structure', PhysicalObjectViews.StructureViewSet)
physicalobjectrouter.register(r'vehicle', PhysicalObjectViews.VehicleViewSet)
physicalobjectrouter.register(r'device', PhysicalObjectViews.DeviceViewSet)

supplierpartnerrouter = AppRouter(root_view_name='app-supplier_partner')
supplierpartnerrouter.register(r'supplier', SupplierPartnerViews.SupplierViewSet)
supplierpartnerrouter.register(r'partner', SupplierPartnerViews.PartnerViewSet)
supplierpartnerrouter.register(r'buyer', SupplierPartnerViews.BuyerViewSet)

informationtechnologyrouter = AppRouter(root_view_name='app-information_technology')
informationtechnologyrouter.register(r'component', ITViews.ComponentViewSet)
informationtechnologyrouter.register(r'component', ITViews.ComponentViewSet)
informationtechnologyrouter.register(r'component_classification', ITViews.ComponentClassificationViewSet)
informationtechnologyrouter.register(r'process_framework', ITViews.ProcessFrameworkViewSet)
informationtechnologyrouter.register(r'process', ITViews.ProcessViewSet)
informationtechnologyrouter.register(r'process_classification', ITViews.ProcessClassificationViewSet)

projectrouter = AppRouter(root_view_name='app-project')
projectrouter.register(r'project', ProjectViews.ProjectViewSet)

router = AppRouter( apps={  'party':'app-party',
                            'location':'app-location',
                            'human_resources':'app-human_resources',
                            'physical_resource':'app-physical_resource',
                            'customer':'app-customer',
                            'credit':'app-credit',
                            'trouble':'app-trouble',
                            'physical_object':'app-physical_object',
                            'supplier_partner':'app-supplier_partner',
                            'information_technology':'app-information_technology', } )
router.register(r'auth/users', UserViewSet)
router.register(r'content_types', ContentTypeViewSet)

appurlpatterns = [
    url(r'^api/party/', include(partyrouter.urls)),
    url(r'^api/location/', include(locationrouter.urls)),
    url(r'^api/human_resources/', include(humanresourcesrouter.urls)),
    url(r'^api/physical_resource/', include(physicalresourcerouter.urls)),
    url(r'^api/customer/', include(customerrouter.urls)),
    url(r'^api/credit/', include(creditrouter.urls)),
    url(r'^api/trouble/', include(troublerouter.urls)),
    url(r'^api/physical_object/', include(physicalobjectrouter.urls)),
    url(r'^api/supplier_partner/', include(supplierpartnerrouter.urls)),
    url(r'^api/information_technology/', include(informationtechnologyrouter.urls)),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + appurlpatterns
