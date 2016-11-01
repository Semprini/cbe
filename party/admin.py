from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.contenttypes.admin import GenericTabularInline

from party.models import Organisation, Individual, PhysicalContact, EmailContact, TelephoneNumber, GenericPartyRole


class GenericPartyRoleAdminForm(forms.ModelForm):
    party = forms.ChoiceField()

    class Meta:
        exclude = []
        model = GenericPartyRole 

    def __init__(self, *args, **kwargs):
        choices = (('',''),)
        for individual in Individual.objects.all():
            choices += (("%d::%s::%s"%(individual.id, individual.__class__.__name__, individual),"%s"%individual),)
        
        for organisation in Organisation.objects.all():
            choices += (("%d::%s::%s"%(organisation.id, organisation.__class__.__name__, organisation),"%s"%organisation),)

        self.base_fields['party'].choices = choices

        forms.ModelForm.__init__(self, *args, **kwargs)
            
        instance = kwargs.get('instance')
        if instance:
            if instance.party:
                print( instance.party )
                self.initial['party'] = "%d::%s::%s"%(instance.party.id,instance.party.__class__.__name__,instance.party)


class PhysicalContactInline(GenericTabularInline):
    model = PhysicalContact
    extra = 0
    ct_field = 'party_role_content_type'
    ct_fk_field = 'party_role_object_id'
    
class EmailContactInline(GenericTabularInline):
    model = EmailContact
    extra = 0
    ct_field = 'party_role_content_type'
    ct_fk_field = 'party_role_object_id'
    
class TelephoneNumberInline(GenericTabularInline):
    model = TelephoneNumber
    extra = 0
    ct_field = 'party_role_content_type'
    ct_fk_field = 'party_role_object_id'

#TODO: Validate the role name vs other roles (E.g. Customer) and force users to admin the correct role.
class GenericPartyRoleAdmin(admin.ModelAdmin):
    list_display = ('party', 'name')
    form = GenericPartyRoleAdminForm
    inlines = [ PhysicalContactInline, EmailContactInline, TelephoneNumberInline]    
    
    def save_model(self, request, obj, form, change):
        splitparty = form.cleaned_data['party'].split('::')
        if splitparty[1] == "Individual":
            obj.party = Individual.objects.get(id=splitparty[0])
        if splitparty[1] == "Organisation":
            obj.party = Organisation.objects.get(id=splitparty[0])
        obj.save()

    
admin.site.register(Organisation)
admin.site.register(Individual)
admin.site.register(PhysicalContact)
admin.site.register(EmailContact)
admin.site.register(TelephoneNumber)
admin.site.register(GenericPartyRole, GenericPartyRoleAdmin)

