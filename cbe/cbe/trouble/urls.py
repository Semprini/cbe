"""cbe trouble URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-trouble')
router.register(r'problem', views.ProblemViewSet)

urlpatterns = [
    url(r'^api/trouble/', include(router.urls)),
]

