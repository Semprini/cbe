from django.db import models

from cbe.customer.models import Customer, CustomerAccount
from cbe.party.models import Organisation
from cbe.location.models import Location

credit_status_choices = (('active', 'active'), ('stop', 'stop'),)

class Credit(models.Model):
    liability_ownership = models.ForeignKey(Organisation, null=True, blank=True, related_name = "credit_liabilities")
    customer = models.ForeignKey(Customer, db_index=True, null=True,blank=True, related_name="credit_liabilities")
    account = models.ForeignKey(CustomerAccount, db_index=True, null=True,blank=True, related_name="credit_liabilities")
    
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    credit_status = models.CharField(max_length=100, choices=credit_status_choices)
    credit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

class CreditProfile(models.Model):
    customer = models.ForeignKey(Customer)
    credit_agency = models.ForeignKey(Organisation,null=True, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    
    credit_risk_rating = models.IntegerField(null=True, blank=True)
    credit_score = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['id']    

        
class CreditAlert(models.Model):
    customer = models.ForeignKey(Customer)
    profile = models.ForeignKey(CreditProfile,null=True, blank=True)
    credit_agency = models.ForeignKey(Organisation,null=True, blank=True)

    alert_type = models.CharField(max_length=300, choices = (('risk', 'risk'), ('threshold', 'threshold'),
                           ('breech', 'breech'), ('other', 'other')))
                           
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['id']
    
    
class CreditBalanceEvent(models.Model):
    customer = models.ForeignKey(Customer)
    account = models.ForeignKey(CustomerAccount)
    credit = models.ForeignKey(Credit)
    
    datetime = models.DateTimeField(auto_now_add=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['id']
    