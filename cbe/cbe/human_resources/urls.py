"""cbe hr URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

import cbe.human_resources.views as HRViews

router = AppRouter(root_view_name='app-human_resources')
router.register(r'staff', HRViews.StaffViewSet)
router.register(r'identification', HRViews.IdentificationViewSet)
router.register(r'identification_type', HRViews.IdentificationTypeViewSet)
router.register(r'timesheet', HRViews.TimesheetViewSet)
router.register(r'timesheet_entries', HRViews.TimesheetEntryViewSet)

urlpatterns = [
    url(r'^api/human_resources/', include(router.urls)),
]

