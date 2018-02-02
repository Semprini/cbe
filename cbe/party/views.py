from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.party.models import Individual, Organisation, TelephoneNumber, GenericPartyRole, Owner, PartyRoleAssociation
from cbe.party.serializers import IndividualSerializer, OrganisationSerializer, TelephoneNumberSerializer, GenericPartyRoleSerializer, OwnerSerializer
from cbe.party.serializers_partyroleassociation import PartyRoleAssociationSerializer

class PartyRoleAssociationViewSet(viewsets.ModelViewSet):
    queryset = PartyRoleAssociation.objects.all()
    serializer_class = PartyRoleAssociationSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    
    
class IndividualViewSet(viewsets.ModelViewSet):
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_fields = ('organisation_type',)
    lookup_field = 'enterprise_id'

class TelephoneNumberViewSet(viewsets.ModelViewSet):
    queryset = TelephoneNumber.objects.all()
    serializer_class = TelephoneNumberSerializer


class GenericPartyRoleViewSet(viewsets.ModelViewSet):
    queryset = GenericPartyRole.objects.all()
    serializer_class = GenericPartyRoleSerializer
