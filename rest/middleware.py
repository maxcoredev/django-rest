import json


class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # If content-type is json and manually navigated in browser:
        # prettify it and wrap with html+body tags, since django-debug-toolbar needs it
        if response['Content-Type'] == 'application/json' and \
           request.environ.get('HTTP_SEC_FETCH_MODE') == 'navigate':
            response['Content-Type'] = 'text/html'
            response.content = json.dumps(json.loads(response.content), sort_keys=True, indent=2, ensure_ascii=False)
            response.content = '<html><body><pre>{}</pre></body></html>'.format(response.content.decode('utf-8'))

        return response