from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from cbe.party.models import PartyRole, Individual, Organisation


class IdentificationType( models.Model ):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.name,)
        

class Identification( models.Model ):
    number = models.CharField(primary_key=True, max_length=200)
    identification_type = models.ForeignKey( IdentificationType )

    party_content_type = models.ForeignKey(
        ContentType, related_name="%(app_label)s_%(class)s_ownership")
    party_object_id = models.PositiveIntegerField()
    party = GenericForeignKey('party_content_type', 'party_object_id')    

    def __str__(self):
        return "{}:{}".format(self.identification_type, self.number,)    


class Staff(PartyRole):
    company = models.ForeignKey(Organisation, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.name is None or self.name == "":
            self.name = "Staff"
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name,)