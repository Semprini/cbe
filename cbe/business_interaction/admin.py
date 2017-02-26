from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericTabularInline

from cbe.business_interaction.models import BusinessInteraction, BusinessInteractionItem, BusinessInteractionRole


# class BusinessInteractionRoleInline(admin.TabularInline):
     # model = BusinessInteractionRole
     # extra = 1


# class BusinessInteractionItemInline(admin.TabularInline):
    # model = BusinessInteractionItem
    # extra = 1


# class BusinessInteractionAdmin(admin.ModelAdmin):
    # list_display = (
        # 'interaction_date', 'interaction_status', 'description', 'place',)
    # inlines = [BusinessInteractionRoleInline, BusinessInteractionItemInline, ]


# class BusinessInteractionItemAdmin(admin.ModelAdmin):
    # list_display = ('business_interaction', 'quantity', 'action', 'place',)


#admin.site.register(BusinessInteraction, BusinessInteractionAdmin)
#admin.site.register(BusinessInteractionItem, BusinessInteractionItemAdmin)
