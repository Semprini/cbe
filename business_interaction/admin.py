from django.contrib import admin

from business_interaction.models import BusinessInteractionRole

class BusinessInteractionRoleInline(admin.TabularInline):
    model = BusinessInteractionRole
    extra = 0
