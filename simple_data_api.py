
def execute(api_request):
    if api_request.get('endpoint', None) == 'test':
        return 'OK'

    return None
