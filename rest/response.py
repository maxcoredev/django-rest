import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from rest.serialize import serialize


class Response(HttpResponse):

    def __init__(self, content=b'', **kwargs):

        content = serialize(content)

        if isinstance(content, (dict, list)):
            kwargs.setdefault('content_type', 'application/json')
            content = json.dumps(content, cls=DjangoJSONEncoder, ensure_ascii=False)

        super().__init__(content, **kwargs)