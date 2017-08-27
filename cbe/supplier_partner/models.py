from django.db import models

from cbe.party.models import PartyRole

class Supplier(PartyRole):
    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Supplier"
        super(Supplier, self).save(*args, **kwargs)

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
        