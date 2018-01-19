from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.credit.models import CreditBalanceEvent, CreditProfile, Credit


class CreditSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Credit
        fields = ('type', 'url', 'liability_ownership', 'customer', 'account', 
                  'credit_limit', 'credit_status','transaction_limit','credit_balance', )

                  
class CreditBalanceEventSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CreditBalanceEvent
        fields = ('type', 'url', 'credit', 'customer', 'account', 'datetime',
                  'amount', 'balance', )


class CreditProfileSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CreditProfile
        fields = ('type', 'url', 'customer', 'credit_agency', 'valid_from', 'valid_to','created',
                  'credit_risk_rating','credit_score',)


