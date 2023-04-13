# pylint: disable=no-member

import importlib
import json
import string

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

def generate_api_token(length=32):
    token = None

    while token is None or APIToken.objects.filter(token=token).count() > 0:
        token = get_random_string(length, allowed_chars=string.ascii_lowercase + string.digits)

    return token

class APIToken(models.Model):
    class Meta: # pylint: disable=too-few-public-methods
        verbose_name = 'API Token'
        verbose_name_plural = 'API Tokens'

    token = models.CharField(max_length=1048576, unique=True, default=generate_api_token)
    responsible_party = models.CharField(max_length=1048576)

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.responsible_party

class APICall(models.Model):
    class Meta: # pylint: disable=too-few-public-methods
        verbose_name = 'API Call'
        verbose_name_plural = 'API Calls'

    when = models.DateTimeField()
    request = models.TextField(max_length=1048576)
    token = models.ForeignKey(APIToken, related_name='api_calls', on_delete=models.CASCADE)
    errored = models.BooleanField(default=False)
    response = models.TextField(max_length=1048576)

    def fetch_request(self):
        return json.loads(self.request)

    def execute(self):
        full_response = {}

        api_request = self.fetch_request()

        for app in settings.INSTALLED_APPS:
            try:
                data_api = importlib.import_module(app + '.simple_data_api')

                response = data_api.execute(api_request)

                if response is not None:
                    full_response[app] = response
            except ImportError:
                pass
            except AttributeError:
                pass

        self.response = json.dumps(full_response, indent=2)
        self.save()

        return full_response
