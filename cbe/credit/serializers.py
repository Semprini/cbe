from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.party.models import Organisation
from cbe.credit.models import CreditBalanceEvent, CreditProfile, Credit, CreditAlert


class CreditSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    liability_ownership = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = Credit
        fields = ('type', 'url', 'liability_ownership', 'customer', 'account', 
                  'credit_limit', 'credit_status','transaction_limit','credit_balance', )

                  
class CreditAlertSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    credit_agency = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = Credit
        fields = ('type', 'url', 'customer', 'profile', 'credit_agency', 
                  'alert_type', 'description',)                  
                  
                  
class CreditBalanceEventSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CreditBalanceEvent
        fields = ('type', 'url', 'credit', 'customer', 'account', 'datetime',
                  'amount', 'balance', )


class CreditProfileSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    credit_agency = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = CreditProfile
        fields = ('type', 'url', 'customer', 'credit_agency', 'valid_from', 'valid_to','created',
                  'credit_risk_rating','credit_score',)


