from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.accounts_receivable.models import CustomerPayment, PaymentChannel
from cbe.customer.serializers import CustomerAccountSerializer

class CustomerPaymentSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    account = CustomerAccountSerializer()
    
    class Meta:
        model = CustomerPayment
        fields = ('type', 'url', 'channel', 'vendor', 'datetime', 
                  'docket_number', 'customer','account','amount','tax' )

                  
class PaymentChannelSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = PaymentChannel
        fields = ('type', 'url', 'name' )