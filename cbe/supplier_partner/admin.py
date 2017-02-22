from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.contenttypes.admin import GenericTabularInline

from cbe.supplier_partner.models import Supplier, Partner, Buyer
from cbe.party.admin import GenericPartyRoleAdmin

admin.site.register(Supplier, GenericPartyRoleAdmin)
admin.site.register(Partner, GenericPartyRoleAdmin)
admin.site.register(Buyer, GenericPartyRoleAdmin)

