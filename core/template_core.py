import re
from core.template_parser import get_template
from project_core.urls import urlpatterns


def page_not_found():
    """
    Возвращаем 404 страницу
    """
    return get_template('404.html')


def request_processor(request, *args, **kwargs):
    """
        Обработка запроса и возпрат ответа
    :param request: запрос
    :param args: аргументы
    :param kwargs: боольше агрументов
    :return:
    """
    for url in urlpatterns:
        matches = re.finditer(url[0], request['PATH_INFO'])
        for match in matches:
            if match:
                kwargs.update(match.groupdict())
                return url[1].view(request, *args, **kwargs)
