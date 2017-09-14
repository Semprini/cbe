import datetime

from django.db import models

from cbe.party.models import Organisation
from cbe.customer.models import Customer, CustomerAccount


class PaymentChannel(models.Model):
    name =  models.CharField( max_length=100 )

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s"%(self.name)

        
class Payment(models.Model):
    channel = models.ForeignKey(PaymentChannel)
    vendor = models.ForeignKey(Organisation, null=True,blank=True)

    datetime = models.DateTimeField(default=datetime.datetime.now)
    docket_number = models.CharField(max_length=50, null=True,blank=True )

    customer = models.ForeignKey(Customer, db_index=True, null=True,blank=True)
    account = models.ForeignKey(CustomerAccount, db_index=True, null=True,blank=True)
    