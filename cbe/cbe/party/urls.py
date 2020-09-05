"""cbe party URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

import cbe.party.views as PartyViews

router = AppRouter(root_view_name='app-party')
router.register(r'individual', PartyViews.IndividualViewSet)
router.register(r'organisation', PartyViews.OrganisationViewSet)
router.register(r'generic_party_role', PartyViews.GenericPartyRoleViewSet)
router.register(r'telephone_number', PartyViews.TelephoneNumberViewSet)
router.register(r'owner', PartyViews.OwnerViewSet)
router.register(r'party_role_association', PartyViews.PartyRoleAssociationViewSet)

urlpatterns = [
    url(r'^api/party/', include(router.urls)),
]

