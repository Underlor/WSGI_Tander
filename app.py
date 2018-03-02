from wsgiref.simple_server import make_server

from core.template_core import get_page


def simple_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    return [get_page(environ)]


with make_server('', 8000, simple_app) as httpd:
    print("Listening on port 8000....")
    httpd.serve_forever()
