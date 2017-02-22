from django.contrib import admin

from cbe.party.admin import GenericPartyRoleAdmin

from cbe.human_resources.models import Staff

admin.site.register(Staff,GenericPartyRoleAdmin)