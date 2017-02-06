from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.sale.models import Sale, SaleItem, Tender, TenderType
from cbe.sale.serializers import SaleSerializer, SaleItemSerializer, TenderSerializer, TenderTypeSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class TenderTypeViewSet(viewsets.ModelViewSet):
    queryset = TenderType.objects.all()
    serializer_class = TenderTypeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
