import collections
import re

from core.Exceptions import IncludeError
from project_core import settings


def get_template(template_file):
    try:
        with open(settings.ROOT_DIR + settings.TEMPLATES_DIR + template_file, 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise IncludeError('Included file "%s" was not found.' % (template_file,))


def get_value_by_keystr(keystr, dictionary):
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


def for_parser(page, context):
    matches = re.finditer(r"{% *for *(\w*\d*) *in *(\w*\d*) *%}([\s|\S]*?)({% *endfor *%})", page)
    for match in matches:
        block_text = ''
        if isinstance(get_value_by_keystr(match.group(2), context), collections.Iterable):
            for item in get_value_by_keystr(match.group(2), context):
                matches_var = re.finditer(r"{{(.+?)}}", match.group(3))
                block_text += match.group(3)
                for match_var in matches_var:
                    block_text = re.sub(
                        r"{{ *%s *}}" % match_var.group(1),
                        str(get_value_by_keystr(''.join(match_var.group(1).strip().split('.')[1:]), item)), block_text)
        page = page.replace(match.group(), block_text)
    return page


def if_parser(page, context):
    regex = r"{% *if *(\d|\w+) *(==|<=|>=|<|>|\!=)? *(\'?\"?[\d|\w]+\'?\"?)? *%}([\s|\S]*?){% *endif *%}"
    matches = re.finditer(regex, page)
    for match in matches:
        block_text = ''
        if match.group(2) is None and match.group(3) is None:
            if get_value_by_keystr(match.group(1), context):
                block_text = match.group(4)
        page = page.replace(match.group(), block_text)
    return page


def var_parser(page, context):
    matches = re.finditer(r"{{(.+?)}}", page)
    for match in matches:
        page = re.sub(r"{{ *%s *}}" % match.group(1), str(get_value_by_keystr(match.group(1).strip(), context)), page)
    return page


def include_parcer(page):
    matches = re.finditer(r"{% *include * [\'|\"](.*)[\'|\"] *%}", page)
    for match in matches:
        page = page.replace(match.group(), get_template(match.group(1)))
    return page


def template_parser(page, context):
    page = include_parcer(page)
    page = for_parser(page, context)
    page = var_parser(page, context)
    page = if_parser(page, context)
    return page
