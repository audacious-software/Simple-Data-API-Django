# pylint: disable=line-too-long

from django.conf.urls import url

from .views import fetch, test_api

urlpatterns = [
    url(r'^test$', test_api, name='api_test'),
    url(r'^fetch$', fetch, name='api_fetch'),
]
