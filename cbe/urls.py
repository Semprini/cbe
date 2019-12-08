"""cbe URL Configuration

"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from drf_nest.routers import AppRouter
from . import views

import cbe.views as CBEViews
import cbe.project.views as ProjectViews

from cbe.party.urls import urlpatterns as PartyUrls
from cbe.location.urls import urlpatterns as LocationUrls
from cbe.accounts_receivable.urls import urlpatterns as ARUrls
from cbe.human_resources.urls import urlpatterns as HRUrls
from cbe.customer.urls import urlpatterns as CustomerUrls
from cbe.supplier_partner.urls import urlpatterns as SPUrls
from cbe.information_technology.urls import urlpatterns as ITUrls
from cbe.resource.urls import urlpatterns as ResourceUrls
from cbe.credit.urls import urlpatterns as CreditUrls
from cbe.trouble.urls import urlpatterns as TroubleUrls
from cbe.physical_object.urls import urlpatterns as PhysicalObjectUrls
from cbe.project.urls import urlpatterns as ProjectUrls

admin.site.site_title = 'CBE'
admin.site.site_header = 'Common Business Entities'

apps={  'party':'app-party',
        'accounts_receivable':'app-accounts_receivable',
        'location':'app-location',
        'human_resources':'app-human_resources',
        'customer':'app-customer',
        'credit':'app-credit',
        'resource':'app-resource',
        'trouble':'app-trouble',
        'physical_object':'app-physical_object',
        'supplier_partner':'app-supplier_partner',
        'project':'app-project',
        'information_technology':'app-information_technology', }
router = AppRouter( apps=apps )
router.register(r'auth/users', CBEViews.UserViewSet)
router.register(r'content_types', CBEViews.ContentTypeViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + PartyUrls + LocationUrls + ARUrls + HRUrls + CustomerUrls + SPUrls + ITUrls + ResourceUrls + CreditUrls + TroubleUrls + PhysicalObjectUrls + ProjectUrls
