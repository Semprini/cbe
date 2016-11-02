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
cberouter.register(r'party/individuals', PartyViews.IndividualViewSet)
cberouter.register(r'party/organisations', PartyViews.OrganisationViewSet)
cberouter.register(r'party/telephone_numbers', PartyViews.TelephoneNumberViewSet)
cberouter.register(r'location/country', LocationViews.CountryViewSet)
cberouter.register(r'location/urban_property_address', LocationViews.UrbanPropertyAddressViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'content_types', ContentTypeViewSet)

for route in cberouter.registry:
    router.register(route[0],route[1])
    
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
