from rest_framework import permissions, renderers, viewsets
from rest_framework.response import Response

from cbe.supplier_partner.models import Supplier, Buyer, Partner, SupplierAccount
from cbe.supplier_partner.serializers import SupplierSerializer, SupplierAccountSerializer, BuyerSerializer, PartnerSerializer



class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class SupplierAccountViewSet(viewsets.ModelViewSet):
    queryset = SupplierAccount.objects.all()
    serializer_class = SupplierAccountSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    

class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    permission_classes = (permissions.DjangoModelPermissions, )


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    