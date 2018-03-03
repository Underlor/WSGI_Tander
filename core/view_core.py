from urllib.parse import parse_qsl

from core.template_parser import template_parser, get_template


def redirect(url, permanent=False):
    return {'redirect_url': url, 'permanent': permanent}


def qs_parser(qs):
    return {item[0]: item[1] for item in parse_qsl(qs)}


class BaseView:
    def __init__(self, template_name=None):
        self.template_name = template_name

    def get(self, request, *args, **kwargs):
        response = ''
        if self.template_name:
            response = template_parser(get_template(self.template_name), kwargs)
        return response

    def post(self, request, *args, **kwargs):
        return ''

    def put(self, request, *args, **kwargs):
        return ''

    def delete(self, request, *args, **kwargs):
        return ''

    def view(self, request, *args, **kwargs):
        if request['REQUEST_METHOD'] == 'GET':
            request['GET'] = parse_qsl(request['QUERY_STRING'])
            return self.get(request, *args, **kwargs)
        elif request['REQUEST_METHOD'] == 'POST':
            request['POST'] = qs_parser(request['wsgi.input'].read(int(request.get('CONTENT_LENGTH', 0))).decode())
            return self.post(request, *args, **kwargs)
        elif request['REQUEST_METHOD'] == 'PUT':
            request['PUT'] = qs_parser(request['wsgi.input'].read(int(request.get('CONTENT_LENGTH', 0))).decode())
            return self.put(request, *args, **kwargs)
        elif request['REQUEST_METHOD'] == 'DELETE':
            request['DELETE'] = qs_parser(request['wsgi.input'].read(int(request.get('CONTENT_LENGTH', 0))).decode())
            return self.delete(request, *args, **kwargs)
