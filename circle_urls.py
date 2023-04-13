import django

from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', django.contrib.admin.site.urls),
    url(r'^api/', include('simple_data_api.urls')),
]
