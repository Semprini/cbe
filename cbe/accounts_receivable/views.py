import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.accounts_receivable.models import CustomerPayment, PaymentChannel
from cbe.accounts_receivable.serializers import CustomerPaymentSerializer, PaymentChannelSerializer

class CustomerPaymentViewSet(viewsets.ModelViewSet):
    queryset = CustomerPayment.objects.all()
    serializer_class = CustomerPaymentSerializer
    
class PaymentChannelViewSet(viewsets.ModelViewSet):
    queryset = PaymentChannel.objects.all()
    serializer_class = PaymentChannelSerializer    
    
    