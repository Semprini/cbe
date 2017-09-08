from django.db import models

from cbe.party.models import PartyRole

class Supplier(PartyRole):
    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Supplier"
        super(Supplier, self).save(*args, **kwargs)

        
class SupplierAccount(models.Model):
    created = models.DateField(auto_now_add=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    
    account_number = models.CharField(primary_key=True, max_length=200)
    supplier = models.ForeignKey(Supplier, related_name="customer_accounts")
    account_status = models.CharField(max_length=100)
    account_type = models.CharField(max_length=200)
    name = models.CharField(max_length=300)
    pin = models.CharField(max_length=100, null=True, blank=True)        
        
        
class Partner(PartyRole):
    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Partner"
        super(Partner, self).save(*args, **kwargs)

class Buyer(PartyRole):
    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Buyer"          
        super(Buyer, self).save(*args, **kwargs)
        