import re
from urllib.parse import unquote
from urllib.parse import parse_qs
from core.template_parser import get_template
from project_core.urls import urlpatterns


def page_not_found():
    return get_template('404.html')


def get_page(request, *args, **kwargs):
    for url in urlpatterns:
        matches = re.finditer(url[0], request['PATH_INFO'])
        for match in matches:
            if match:
                kwargs.update(match.groupdict())
                return url[1].view(request, *args, **kwargs)
