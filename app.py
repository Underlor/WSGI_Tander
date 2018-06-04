from wsgiref.simple_server import make_server

from core.template_core import request_processor, page_not_found
from project_core import settings


def app(environ, start_response):
    response = request_processor(environ)
    if response is None:
        response = page_not_found()
        start_response('404 Not Found', [('Content-type', 'text/html')])
    elif 'redirect_url' in response:
        if response.get('permanent', False):
            start_response('301 Moved Permanently', [('Location', response.get('redirect_url', '/'))])
        else:
            start_response('302 Moved', [('Location', response.get('redirect_url', '/'))])
        return []
    else:
        start_response('200 OK', [('Content-type', 'text/html')])
    return [response.encode()]


if __name__ == "__main__":
    with make_server(settings.IP, settings.PORT, app) as httpd:
        print("Listening on port 8000....")
        httpd.serve_forever()
