from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from gm2m import GM2MField

class ContactMedium(models.Model):
    # TODO: Restrict to PartyRole derrived types
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    party_role_content_type = models.ForeignKey(
        ContentType, 
        null=True)
    party_role_object_id = models.PositiveIntegerField(null=True)
    party_role = GenericForeignKey(
        'party_role_content_type', 'party_role_object_id',
        )

    class Meta:
        abstract = True


class TelephoneNumber(ContactMedium):
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class EmailContact(ContactMedium):
    email_address = models.EmailField(max_length=200)  # , unique=True)

    def __str__(self):
        return self.email_address


class PhysicalContact(ContactMedium):
    # TODO: Restrict to Address derrived types
    address_content_type = models.ForeignKey(
        ContentType, related_name="%(app_label)s_%(class)s_address_ownership")
    address_object_id = models.PositiveIntegerField()
    address = GenericForeignKey('address_content_type', 'address_object_id')
