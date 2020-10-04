from django.contrib import admin
from django import forms
from django.db import models

from cbe.location.models import GeographicArea, UrbanPropertyAddress, UrbanPropertySubAddress, PoBoxAddress, RuralPropertyAddress, Location, Country, City


class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)
    actions = ['country_geo_data', ]

    def country_geo_data(self, request, queryset):
        self.message_user(request, "Working on geo data in the background...")
        # TODO: Async processing
        for country in queryset:
            country.country_geo_data()
    country_geo_data.short_description = "Create geographic data for selected countries"


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(UrbanPropertyAddress)
admin.site.register(UrbanPropertySubAddress)
admin.site.register(PoBoxAddress)
admin.site.register(RuralPropertyAddress)
admin.site.register(Location)
admin.site.register(GeographicArea)