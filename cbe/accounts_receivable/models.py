import datetime

import django
from django.db import models

from cbe.party.models import Organisation
from cbe.customer.models import Customer, CustomerAccount


class PaymentChannel(models.Model):
    name =  models.CharField( max_length=100 )

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s"%(self.name)

        
class CustomerPayment(models.Model):
    channel = models.ForeignKey(PaymentChannel, on_delete=django.db.models.deletion.CASCADE)
    vendor = models.ForeignKey(Organisation, on_delete=django.db.models.deletion.CASCADE, null=True,blank=True)

    datetime = models.DateTimeField(default=datetime.datetime.now)
    docket_number = models.CharField(max_length=50, null=True,blank=True )

    customer = models.ForeignKey(Customer, on_delete=django.db.models.deletion.CASCADE, db_index=True, null=True,blank=True)
    account = models.ForeignKey(CustomerAccount, on_delete=django.db.models.deletion.CASCADE, db_index=True, null=True,blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    