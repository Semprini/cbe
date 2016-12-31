from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericTabularInline

from cbe.party.models import Organisation, Individual, PhysicalContact, EmailContact, TelephoneNumber, GenericPartyRole
from cbe.party.admin import GenericPartyRoleAdminForm, GenericPartyRoleAdmin, PhysicalContactInline, EmailContactInline, TelephoneNumberInline
from cbe.business_interaction.admin import BusinessInteractionRoleInline
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountRelationship, CustomerOrder, CustomerAccountContact


class CustomerAdminForm(GenericPartyRoleAdminForm):

    class Meta:
        exclude = ['contact_mediums',]
        model = Customer


class CustomerAccountAdminForm(forms.ModelForm):
    customer_account_contact = forms.ChoiceField(required=False)

    class Meta:
        exclude = ['contact_content_type', 'contact_object_id']
        model = CustomerAccount

    def __init__(self, *args, **kwargs):
        choices = (('', ''),)
        for role in GenericPartyRole.objects.all():
            choices += (("%d::%s::%s" % (role.id, role.__class__.__name__,
                                         role), "%s : %s" % (role.name, role.party)),)

        self.base_fields['customer_account_contact'].choices = choices

        forms.ModelForm.__init__(self, *args, **kwargs)

        #instance = kwargs.get('instance')
        # if instance:
        #    if instance.customer_account_contact:
        # TODO: MANY TO MANY
        #        self.initial['customer_account_contact'] = "%d::%s::%s"%(instance.customer_account_contact.id,instance.customer_account_contact.__class__.__name__,instance.customer_account_contact)


class AccountInline(admin.TabularInline):
    model = CustomerAccount
    extra = 0


class CustomerAdmin(GenericPartyRoleAdmin):
    list_display = ('customer_number', 'customer_status', 'party',)
    form = CustomerAdminForm
    fields = (
        'valid_to', 'name', 'party', 'customer_number', 'customer_status')
    readonly_fields = ('name', 'party_content_type', 'party_object_id')
    inlines = [AccountInline, PhysicalContactInline,
               EmailContactInline, TelephoneNumberInline]


class CustomerAccountContactAdmin(GenericPartyRoleAdmin):
    list_display = ('name', 'party',)
    #form = CustomerAdminForm
    #readonly_fields = ('name', 'party_content_type', 'party_object_id')
    inlines = [PhysicalContactInline,
               EmailContactInline, TelephoneNumberInline]


class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = (
        'customer', 'account_number', 'name', 'account_status', 'credit_limit')
    #form = CustomerAccountAdminForm

    # def save_model(self, request, obj, form, change):
    #splitrole = form.cleaned_data['customer_account_contact'].split('::')
    # print(splitrole)
    # if len(splitrole) > 1:
    #    obj_type = ContentType.objects.get(model=splitrole[1].lower())  #TODO: Use correct content type in form (lower is error prone)
    #    obj.contact_content_type = obj_type
    #    obj.contact_object_id = splitrole[0]
    # obj.save()


class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = (
        'interaction_date', 'interaction_status', 'customer_order_type')
    inlines = [BusinessInteractionRoleInline, ]


admin.site.register(CustomerOrder, CustomerOrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerAccount, CustomerAccountAdmin)
admin.site.register(CustomerAccountRelationship)
admin.site.register(CustomerAccountContact, CustomerAccountContactAdmin)
