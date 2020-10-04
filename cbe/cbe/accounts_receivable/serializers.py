from rest_framework import serializers

from drf_nest.serializer_fields import TypeField
from cbe.party.models import Organisation
from cbe.accounts_receivable.models import CustomerPayment, PaymentChannel
from cbe.customer.serializers import CustomerAccountSerializer

class CustomerPaymentSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    account = CustomerAccountSerializer()
    vendor = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())
    
    class Meta:
        model = CustomerPayment
        fields = ('type', 'url', 'channel', 'vendor', 'datetime', 
                  'docket_number', 'customer','account','amount','tax' )

                  
class PaymentChannelSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = PaymentChannel
        fields = ('type', 'url', 'name' )