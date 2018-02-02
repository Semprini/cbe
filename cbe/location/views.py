from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.location.models import GeographicArea, UrbanPropertyAddress, UrbanPropertySubAddress, RuralPropertyAddress, PoBoxAddress, Location, Country, City
from cbe.location.serializers import GeographicAreaSerializer, UrbanPropertyAddressSerializer, CountrySerializer, PoBoxAddressSerializer, CitySerializer, LocationSerializer


class GeographicAreaViewSet(viewsets.ModelViewSet):
    queryset = GeographicArea.objects.all()
    serializer_class = GeographicAreaSerializer
        
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class UrbanPropertyAddressViewSet(viewsets.ModelViewSet):
    queryset = UrbanPropertyAddress.objects.all()
    serializer_class = UrbanPropertyAddressSerializer

class PoBoxAddressViewSet(viewsets.ModelViewSet):
    queryset = PoBoxAddress.objects.all()
    serializer_class = PoBoxAddressSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
