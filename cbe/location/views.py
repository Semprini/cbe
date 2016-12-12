from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.location.models import UrbanPropertyAddress, UrbanPropertySubAddress, RuralPropertyAddress, PoBoxAddress, AbsoluteLocalLocation, Country, City
from cbe.location.serializers import UrbanPropertyAddressSerializer, CountrySerializer, PoBoxAddressSerializer, CitySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    
class UrbanPropertyAddressViewSet(viewsets.ModelViewSet):
    queryset = UrbanPropertyAddress.objects.all()
    serializer_class = UrbanPropertyAddressSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    #                      IsOwnerOrReadOnly,)

    
class PoBoxAddressViewSet(viewsets.ModelViewSet):
    queryset = PoBoxAddress.objects.all()
    serializer_class = PoBoxAddressSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    #                      IsOwnerOrReadOnly,)    
