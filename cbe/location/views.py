from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.location.models import UrbanPropertyAddress, UrbanPropertySubAddress, RuralPropertyAddress, PoBoxAddress, AbsoluteLocalLocation, Country
from cbe.location.serializers import UrbanPropertyAddressSerializer, CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    
class UrbanPropertyAddressViewSet(viewsets.ModelViewSet):
    queryset = UrbanPropertyAddress.objects.all()
    serializer_class = UrbanPropertyAddressSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    #                      IsOwnerOrReadOnly,)

