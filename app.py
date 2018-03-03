from wsgiref.simple_server import make_server

from core.template_core import get_page, page_not_found
from project_core import settings


def app(environ, start_response):
    page = get_page(environ)
    if not page:
        page = page_not_found().encode()
        start_response('404 Not Found', [('Content-type', 'text/html')])
    else:
        start_response('200 OK', [('Content-type', 'text/html')])
    return [page]


if __name__ == "__main__":
    with make_server(settings.IP, settings.PORT, app) as httpd:
        print("Listening on port 8000....")
        httpd.serve_forever()
