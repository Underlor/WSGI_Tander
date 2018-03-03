import re
from urllib.parse import unquote

from core.template_parser import template_parser, get_template
from project_core.urls import urlpatterns




def page_not_found():
    return get_template('404.html')


def get_page(request, *args, **kwargs):
    if request['QUERY_STRING']:
        request['GET'] = {}
        arr = request['QUERY_STRING'].split('&')
        for element in arr:
            a = element.split('=')
            request['GET'][a[0]] = unquote(a[1])

    for url in urlpatterns:
        matches = re.finditer(url[0], request['PATH_INFO'])
        for match in matches:
            if match:
                kwargs.update(match.groupdict())
                context = url[1]().view(request, *args, **kwargs)
                page = template_parser(get_template(url[2]), context)
                return page.encode()
