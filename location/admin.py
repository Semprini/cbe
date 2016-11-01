from django.contrib import admin
from django import forms
from django.db import models

from location.models import UrbanPropertyAddress, UrbanPropertySubAddress, PoBoxAddress, RuralPropertyAddress, AbsoluteLocalLocation, Country


admin.site.register(Country)
admin.site.register(UrbanPropertyAddress)
admin.site.register(UrbanPropertySubAddress)
admin.site.register(PoBoxAddress)
admin.site.register(RuralPropertyAddress)
admin.site.register(AbsoluteLocalLocation)

