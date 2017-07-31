from django.db.models import Q

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

#from cbe.permissions import IsOwnerOrReadOnly
from cbe.party.models import Individual, Organisation
from cbe.human_resources.models import Staff
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountContact
from cbe.customer.serializers import CustomerAccountContactSerializer, CustomerSerializer, CustomerAccountSerializer

#from expand.views import ExpandModelViewSet


class CustomerViewSet(viewsets.ModelViewSet):
    #queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    #                      IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()
        else:
            # Check if the user has an indiviual object, if not return unmanaged customers only
            individuals = Individual.objects.filter(user=self.request.user)
            if len( individuals ) != 1:
                return Customer.objects.filter(managed_by=None)
                
            # Find organisations where the individual is on staff
            staffs = Staff.objects.filter( party_content_type__model='individual', party_object_id=individuals[0].pk )
            organisations = []
            for staff in staffs:
                organisations.append( staff.company )
            
            return Customer.objects.filter( Q(managed_by__in=organisations) | Q(managed_by=None) )
        
        
    # def perform_create(self, serializer):
    #    serializer.save(owner=self.request.user)


class CustomerAccountViewSet(viewsets.ModelViewSet):
    queryset = CustomerAccount.objects.all()
    serializer_class = CustomerAccountSerializer


class CustomerAccountContactViewSet(viewsets.ModelViewSet):
    queryset = CustomerAccountContact.objects.all()
    serializer_class = CustomerAccountContactSerializer
