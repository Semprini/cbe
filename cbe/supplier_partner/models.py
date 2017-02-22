from django.db import models

from cbe.party.models import PartyRole

class Supplier(PartyRole):
    def save(self, *args, **kwargs):
        self.name = "Supplier"
        super(Supplier, self).save(*args, **kwargs)

class Partner(PartyRole):
    def save(self, *args, **kwargs):
        self.name = "Partner"
        super(Partner, self).save(*args, **kwargs)

class Buyer(PartyRole):
    def save(self, *args, **kwargs):
        self.name = "Buyer"
        super(Buyer, self).save(*args, **kwargs)
        