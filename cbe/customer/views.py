from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
#from cbe.permissions import IsOwnerOrReadOnly
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountContact
from cbe.customer.serializers import CustomerAccountContactSerializer, CustomerSerializer, CustomerAccountSerializer

#from expand.views import ExpandModelViewSet


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    #                      IsOwnerOrReadOnly,)

    # def perform_create(self, serializer):
    #    serializer.save(owner=self.request.user)


class CustomerAccountViewSet(viewsets.ModelViewSet):
    queryset = CustomerAccount.objects.all()
    serializer_class = CustomerAccountSerializer


class CustomerAccountContactViewSet(viewsets.ModelViewSet):
    queryset = CustomerAccountContact.objects.all()
    serializer_class = CustomerAccountContactSerializer
