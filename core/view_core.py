from urllib.parse import parse_qsl

from core.template_parser import get_template, TemplateParser


def redirect(url, permanent=False):
    """
    Редиррект
    P.S. Он работает, честно, но я не придумал где его тут использовать :)
    :param url:  Ссылка на которую пересылаем
    :param permanent: Передает браузеру код перманентного перехода. Браузер не запомнит url c которого его перебросило
    """
    return {'redirect_url': url, 'permanent': permanent}


def qs_parser(qs):
    """
    Доработка парсера из urllib
    :param qs: строка формата 'ключ=значение'
    :return: словарь на основе строки
    """
    return {item[0]: item[1] for item in parse_qsl(qs)}


class BaseView:
    """
    Основной клас View
    Основа обработки запросов клиента
    """
    def __init__(self, template_name=None):
        self.template_name = template_name

    def get(self, request, *args, **kwargs):
        response = ''
        if self.template_name:
            response = TemplateParser(get_template(self.template_name), kwargs).template
        return response

    def post(self, request, *args, **kwargs):
        return ''

    def put(self, request, *args, **kwargs):
        return ''

    def delete(self, request, *args, **kwargs):
        return ''

    def view(self, request, *args, **kwargs):
        """
            Обработчик запросов
        :param request: запрос
        :param args: аргументы
        :param kwargs: еще больше аргументов
        :return: ответ клиенту
        """
        if request['REQUEST_METHOD'].upper() == 'GET':
            request['GET'] = parse_qsl(request['QUERY_STRING'])
            return self.get(request, *args, **kwargs)
        elif request['REQUEST_METHOD'].upper() == 'POST':
            request['POST'] = qs_parser(request['wsgi.input'].read(int(request.get('CONTENT_LENGTH', 0))).decode())
            return self.post(request, *args, **kwargs)
        elif request['REQUEST_METHOD'].upper() == 'PUT':
            request['PUT'] = qs_parser(request['wsgi.input'].read(int(request.get('CONTENT_LENGTH', 0))).decode())
            return self.put(request, *args, **kwargs)
        elif request['REQUEST_METHOD'].upper() == 'DELETE':
            request['DELETE'] = qs_parser(request['wsgi.input'].read(int(request.get('CONTENT_LENGTH', 0))).decode())
            return self.delete(request, *args, **kwargs)
