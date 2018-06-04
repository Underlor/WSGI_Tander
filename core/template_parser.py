import collections
import re

from core.Exceptions import IncludeError
from project_core import settings


def get_value_by_keystr(keystr, dictionary):
    """
        Функция для обработки переменных шаблона как в Jinja
    :param keystr: строка с цепочкой переменных через '.'
    :param dictionary: словарь для обработки цепочки
    :return: искомая перменная
    """
    for key in keystr.split('.'):
        if isinstance(dictionary, dict):
            try:
                if key in dictionary:
                    dictionary = dictionary.get(key, '')
                elif int(key) in dictionary:
                    dictionary = dictionary.get(int(key), '')
            except ValueError:
                dictionary = ''
        elif isinstance(dictionary, (set, list,)):
            try:
                dictionary = dictionary[int(key)]
            except ValueError:
                dictionary = ''
    return dictionary


class TemplateParser:
    """
        Парсер шаблона. Да сырой. Да глупый. Но регулярные выражения не дали больше возможностей для него.
        Идея взята с Jinja. Реализация не взята, но я пытался :)
    """
    def __init__(self, template, context):
        self.template = template
        self.context = context
        self.parse()

    def for_parser(self):
        """
            Обработка циклов шаблона
        """
        matches = re.finditer(r"{% *for *(\w*\d*) *in *(\w*\d*) *%}([\s|\S]*?)({% *endfor *%})", self.template)
        for match in matches:
            block_text = ''
            if isinstance(get_value_by_keystr(match.group(2), self.context), collections.Iterable):
                counter = 0
                for item in get_value_by_keystr(match.group(2), self.context):
                    block_text += match.group(3)
                    counter += 1
                    matches_counter = re.finditer(r"{% *counter *%}", match.group(3))
                    for match_counter in matches_counter:
                        block_text = block_text.replace(match_counter.group(), str(counter))
                    matches_var = re.finditer(r"{{(.+?)}}", match.group(3))
                    for match_var in matches_var:
                        block_text = block_text.replace(
                            match_var.group(),
                            str(get_value_by_keystr(''.join(match_var.group(1).strip().split('.')[1:]), item))
                        )
            self.template = self.template.replace(match.group(), block_text)

    def if_parser(self):
        """
            Обработка логических ветвлений
        """
        regex = r"{% *if *([\w\d\.]*) *%}([\S\s]*?){% *else *%}([\S\s]*?){% *endif *%}"
        matches = re.finditer(regex, self.template)
        for match in matches:
            if get_value_by_keystr(match.group(1), self.context):
                self.template = self.template.replace(match.group(), match.group(2))
            else:
                self.template = self.template.replace(match.group(), match.group(3))
        regex = r"{% *if *([\w\d\.]*) *%}([\S\s]*?){% *endif *%}"
        matches = re.finditer(regex, self.template)
        for match in matches:
            if get_value_by_keystr(match.group(1), self.context):

                self.template = self.template.replace(match.group(), match.group(2))
            else:
                self.template = self.template.replace(match.group(), '')

    def var_parser(self):
        """
            Обработка переменных
        """
        matches = re.finditer(r"{{(.+?)}}", self.template)
        for match in matches:
            self.template = re.sub(r"{{ *%s *}}" % match.group(1),
                                   str(get_value_by_keystr(match.group(1).strip(), self.context)),
                                   self.template)

    def include_parcer(self):
        """
            Парсер подключений шаблонов
        """
        matches = re.finditer(r"{% *include * [\'|\"](.*)[\'|\"] *%}", self.template)
        for match in matches:
            self.template = self.template.replace(match.group(), get_template(match.group(1)))
            self.if_parser()

    def parse(self):
        self.include_parcer()
        self.for_parser()
        self.var_parser()
        self.if_parser()


def get_template(template_file):
    """
        Получение шаблона из файла
    :param template_file: путь к файлу с шаблоном
    :return: текст из файла
    """
    try:
        with open(settings.ROOT_DIR + settings.TEMPLATES_DIR + template_file, 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise IncludeError('Included file "%s" was not found.' % (template_file,))
