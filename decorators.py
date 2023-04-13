# pylint: disable=no-member

import base64

from django.http import HttpResponse

from .models import APIToken

# via https://stackoverflow.com/a/47902577/193812

def basic_auth(view):
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()

            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    username, password = base64.b64decode(auth[1]).decode('utf8').split(':', 1) # pylint: disable=unused-variable

                    matched_token = APIToken.objects.filter(token=password).first()

                    if matched_token is not None:
                        return view(request, *args, **kwargs)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="API Access"'

        return response

    return wrap
