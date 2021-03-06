import django
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from gm2m import GM2MField

from cbe.location.models import Country
from cbe.party.models_contact_medium import ContactMedium, TelephoneNumber, EmailContact, PhysicalContact
from cbe.resource.models import PhysicalResource, LogicalResource

GENDER_CHOICES = (('Undisclosed', 'Undisclosed'),
                  ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
MARITAL_STATUS_CHOICES = (('Undisclosed', 'Undisclosed'),
                          ('Single', 'Single'), ('Married', 'Married'), ('Other', 'Other'))


    
class Party(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True


class Individual(Party):
    user = models.ForeignKey(User, on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    gender = models.CharField(
        max_length=50, blank=True, null=True, choices=GENDER_CHOICES)
    family_names = models.CharField(max_length=200, blank=True)
    given_names = models.CharField(max_length=200, blank=True)
    middle_names = models.CharField(max_length=200, blank=True)
    form_of_address = models.CharField(max_length=100, blank=True)
    legal_name = models.CharField(max_length=200, blank=True)
    marital_status = models.CharField(
        max_length=100, null=True, blank=True, choices=MARITAL_STATUS_CHOICES)
    nationality = models.ForeignKey(Country, on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    place_of_birth = models.CharField(max_length=200, blank=True)

    identifiers = GenericRelation('human_resources.Identification', object_id_field="party_object_id", content_type_field='party_content_type', related_query_name='individual')    

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        form = ""
        if self.form_of_address != "":
            form = self.form_of_address + " "
        if self.middle_names != "":
            self.name = form + \
                " ".join(
                    [self.given_names, self.middle_names, self.family_names])
        elif self.given_names != "":
            self.name = form + " ".join([self.given_names, self.family_names])

        super(Individual, self).save(*args, **kwargs)


class Organisation(Party):  # Eg IRD
    parent = models.ForeignKey('Organisation', on_delete=django.db.models.deletion.CASCADE, blank=True, null=True, related_name='sub_organisations')
    enterprise_id = models.IntegerField(null=True)
    code = models.CharField(max_length=200, blank=True, null=True)
    organisation_type = models.CharField(max_length=200, blank=True, null=True)

    identifiers = GenericRelation('human_resources.Identification', object_id_field="party_object_id", content_type_field='party_content_type', related_query_name='organisation')    
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.name


class PartyRoleAssociation(models.Model):
    valid_from = models.DateTimeField(default=now, null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    association_type = models.CharField(max_length=200)
    
    association_from_content_type = models.ForeignKey(
        ContentType, on_delete=django.db.models.deletion.CASCADE, related_name="%(app_label)s_%(class)s_from")
    association_from_object_id = models.CharField(max_length=200)
    association_from = GenericForeignKey('association_from_content_type', 'association_from_object_id')

    association_to_content_type = models.ForeignKey(
        ContentType, on_delete=django.db.models.deletion.CASCADE, related_name="%(app_label)s_%(class)s_to")
    association_to_object_id = models.CharField(max_length=200)
    association_to = GenericForeignKey('association_to_content_type', 'association_to_object_id')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s %s:%s" % (self.association_type, self.association_to_content_type, self.association_to)    

        
class PartyRole(models.Model):
    valid_from = models.DateTimeField(default=now, null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, null=True)
    
    individual = models.ForeignKey(Individual, on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)

    associations_from = GenericRelation(PartyRoleAssociation, 
                                        object_id_field="association_from_object_id", content_type_field='association_from_content_type',)
    associations_to = GenericRelation(PartyRoleAssociation, 
                                        object_id_field="association_to_object_id", content_type_field='association_to_content_type')

    #telephone_numbers = GenericRelation(TelephoneNumber,object_id_field="party_role_object_id", content_type_field='party_role_content_type')
    #email_contacts = GenericRelation(EmailContact,object_id_field="party_role_object_id", content_type_field='party_role_content_type')
    #physical_contacts = GenericRelation(PhysicalContact,object_id_field="party_role_object_id", content_type_field='party_role_content_type')
    identifiers = GenericRelation('human_resources.Identification', 
                                       object_id_field="party_role_object_id", content_type_field='party_role_content_type',)    

    physical_contacts = models.ManyToManyField(PhysicalContact, blank=True, related_name="%(app_label)s_%(class)s_physical_contacts" )
    telephone_numbers = models.ManyToManyField(TelephoneNumber, blank=True, related_name="%(app_label)s_%(class)s_telephone_numbers" )
    email_contacts = models.ManyToManyField(EmailContact, blank=True, related_name="%(app_label)s_%(class)s_email_contacts" )
    
    physical_resources = models.ManyToManyField(PhysicalResource, blank=True, related_name="%(app_label)s_%(class)s_physical_resources" )
    logical_resources = models.ManyToManyField(LogicalResource, blank=True, related_name="%(app_label)s_%(class)s_logical_resources" )

    class Meta:
        abstract = True

    def __setattr__(self, attrname, val):
        super(PartyRole, self).__setattr__(attrname, val)
        if attrname == "organisation" and val != None:
            self.individual = None
        elif attrname == "individual" and val != None:
            self.organisation = None
            
    @property
    def party(self):
        if self.individual is None:
            return self.organisation
        return self.individual

    @party.setter
    def party(self, value):
        if type(value) is Individual or value == None:
            self.individual = value
            self.organisation = None
        else:
            self.organisation = value
            self.individual = None
    
    #@property
    #def individual(self):
    #    if type(self.party) is Individual:
    #        return self.party

    #@individual.setter
    #def individual(self, value):
    #    if type(value) is Individual or value == None:
            # self.party = value
        # else:
            # raise Exception(
                # "Invalid type of party provided as individual to PartyRole: %s" % type(value))

    # @property
    # def organisation(self):
        # if type(self.party) is Organisation:
            # return self.party

    # @organisation.setter
    # def organisation(self, value):
        # if type(value) is Organisation or value == None:
            # self.party = value
        # else:
            # raise Exception(
                # "Invalid type of party provided as organisation to PartyRole: %s" % type(value))

    def __str__(self):
        return "%s as a %s" % (self.party, self.name)

    
class GenericPartyRole(PartyRole):
    class Meta:
        ordering = ['id']

    
class Owner(PartyRole):

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Owner"          
        super(Owner, self).save(*args, **kwargs)

        
