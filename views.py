# pylint: disable=no-member, line-too-long

import base64
import json
import sys
import traceback

import six

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .decorators import basic_auth
from .models import APIToken, APICall

def create_api_call(request, endpoint):
    # Via https://stackoverflow.com/a/38044377/193812

    auth_header = request.META.get('HTTP_AUTHORIZATION', None)

    if auth_header is not None:

        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials

        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')

        password = decoded_credentials[1]

        matched_token = APIToken.objects.filter(token=password).first()

        if matched_token is None:
            raise PermissionDenied()

        request_dict = {
            'endpoint': endpoint
        }

        request_dict['META'] = dict(request.META)
        request_dict['GET'] = dict(request.GET)
        request_dict['POST'] = dict(request.POST)

        return APICall.objects.create(when=timezone.now(), request=json.dumps(request_dict, indent=2, default=str), token=matched_token)

    raise PermissionDenied()


@csrf_exempt
@basic_auth
def fetch(request): # pylint: disable=unused-argument
    api_call = create_api_call(request, 'fetch')

    try:
        results = api_call.execute()

        return HttpResponse(json.dumps(results, indent=2), content_type='application/json', status=200)
    except: # pylint: disable=bare-except
        exc_type, exc_value, exc_traceback = sys.exc_info()

        api_call.errored = True
        api_call.response = traceback.format_exc()
        api_call.save()

        six.reraise(exc_type, exc_value, exc_traceback)

    raise Exception('Error processing API call. Check logs for details.') # pylint: disable=broad-exception-raised

@csrf_exempt
@basic_auth
def test_api(request): # pylint: disable=unused-argument
    api_call = create_api_call(request, 'test')

    try:
        results = api_call.execute()

        return HttpResponse(json.dumps(results, indent=2), content_type='application/json', status=200)
    except: # pylint: disable=bare-except
        exc_type, exc_value, exc_traceback = sys.exc_info()

        api_call.errored = True
        api_call.response = traceback.format_exc()
        api_call.save()

        six.reraise(exc_type, exc_value, exc_traceback)

    raise Exception('Error processing API call. Check logs for details.') # pylint: disable=broad-exception-raised
