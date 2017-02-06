from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.sale.models import Sale, SaleItem, TenderType, Tender


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Sale
        fields = ('type', 'url', 'store', 'datetime', 'docket_number',
                  'total_amount', 'total_discount', 'customer', 'id_type','id_number','promotion','tenders','sale_items',)


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SaleItem
        fields = ('type', 'url', 'sale', 'product', 'amount',
                  'discount','promotion' )


class TenderTypeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = TenderType
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name',
                  'description', )


class TenderSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Tender
        fields = ('type', 'url', 'sale', 'tender_type', 'amount',
                  'reference', )