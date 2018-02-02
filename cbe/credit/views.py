import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.credit.models import CreditBalanceEvent, CreditProfile, Credit, CreditAlert
from cbe.credit.serializers import CreditBalanceEventSerializer, CreditProfileSerializer, CreditSerializer, CreditAlertSerializer

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

class CreditAlertViewSet(viewsets.ModelViewSet):
    queryset = CreditAlert.objects.all()
    serializer_class = CreditAlertSerializer
    
class CreditBalanceEventViewSet(viewsets.ModelViewSet):
    queryset = CreditBalanceEvent.objects.all()
    serializer_class = CreditBalanceEventSerializer

class CreditProfileViewSet(viewsets.ModelViewSet):
    queryset = CreditProfile.objects.all()
    serializer_class = CreditProfileSerializer
    