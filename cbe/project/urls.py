"""cbe project URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-project')
router.register(r'project', views.ProjectViewSet)

urlpatterns = [
    url(r'^api/project/', include(router.urls)),
]

