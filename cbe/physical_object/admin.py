from django.contrib import admin

from cbe.physical_object.models import Structure, Vehicle

class Structure_ModelAdmin(admin.ModelAdmin):
    list_display        = ('start_date','end_date','physical_object_type','make',)
    list_display_links  = ('physical_object_type','make',)
    list_filter         = ['make',]

    
class Vehicle_ModelAdmin(admin.ModelAdmin):
    list_display        = ('start_date','end_date','physical_object_type','make','series','model','year')
    list_display_links  = ('physical_object_type','make','series','model')
    list_filter         = ['make','series']

    
admin.site.register(Structure,Structure_ModelAdmin)
admin.site.register(Vehicle,Vehicle_ModelAdmin)