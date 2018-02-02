from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericTabularInline

from cbe.party.models import Organisation, Individual, PhysicalContact, EmailContact, TelephoneNumber, GenericPartyRole
from cbe.party.admin import GenericPartyRoleAdminForm, GenericPartyRoleAdmin
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountRelationship, CustomerAccountContact


class CustomerAdminForm(GenericPartyRoleAdminForm):

    class Meta:
        exclude = ['contact_mediums',]
        model = Customer


class AccountInline(admin.TabularInline):
    model = CustomerAccount
    extra = 0


class CustomerAdmin(GenericPartyRoleAdmin):
    list_display = ('customer_number', 'customer_status', 'party',)
    form = CustomerAdminForm
    fields = (
        'valid_to', 'name', 'party', 'customer_number', 'customer_status', 'managed_by')
    readonly_fields = ('name',)
    inlines = [AccountInline, ]

class CustomerAccountContactAdmin(GenericPartyRoleAdmin):
    list_display = ('name', 'party',)
    #form = CustomerAdminForm
    #readonly_fields = ('name', 'party_content_type', 'party_object_id')


class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = (
        'customer', 'account_number', 'name', 'account_status', )




admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerAccount, CustomerAccountAdmin)
admin.site.register(CustomerAccountRelationship)
admin.site.register(CustomerAccountContact, CustomerAccountContactAdmin)
