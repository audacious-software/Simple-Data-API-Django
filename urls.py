# pylint: disable=line-too-long

import sys

if sys.version_info[0] > 2:
    from django.urls import re_path as url # pylint: disable=no-name-in-module
else:
    from django.conf.urls import url

from .views import fetch, test_api

urlpatterns = [
    url(r'^test$', test_api, name='api_test'),
    url(r'^fetch$', fetch, name='api_fetch'),
]
