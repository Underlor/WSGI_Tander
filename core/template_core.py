import operator
import re

operator_lookup_table = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}


def get_value_by_keystr(keystr, dictionary):
    keystr = keystr.split('.')
    for key in keystr:
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


def for_parser(page, context, array=None, arrname=''):
    matches = re.finditer(r"{% *for *(\w*\d*) *in *(\w*\d*) *%}(\s*.*\s*){% *endfor *%}", page, re.DOTALL)
    for match in matches:
        block_text = ''
        if isinstance(array, (set, list)) and arrname == match.group(2):
            for item in array:
                block_text += match.group(3).replace('{{%s}}' % match.group(1), str(item))
                block_text = for_parser(block_text, context, item, match.group(1))
        else:
            for item in get_value_by_keystr(match.group(2), context):
                block_text += match.group(3).replace('{{%s}}' % match.group(1), str(item))
                block_text = for_parser(block_text, context, item, match.group(1))
        page = page.replace(match.group(), block_text)
    return page


def if_parser(page, context):
    regex = r"{% *if *(\d|\w+) *(==|<=|>=|<|>|\!=)? *(\'?\"?[\d|\w]+\'?\"?)? *%}(\s*.*\s*){% *endif *%}"
    matches = re.finditer(regex, page)
    for match in matches:
        block_text = ''
        if match.group(2) is None and match.group(3) is None:
            if get_value_by_keystr(match.group(1), context):
                block_text = match.group(4)
        else:
            if match.group(2) in operator_lookup_table:
                var1 = match.group(1)
                var2 = match.group(3)
                if "'" in var1 or '"' in var1:
                    var1 = var1[1:-1]
                if "'" in var2 or '"' in var2:
                    var2 = var2[1:-1]

                if operator_lookup_table[match.group(2)](get_value_by_keystr(var1, context),
                                                         get_value_by_keystr(var2, context)):
                    block_text = match.group(4)
                try:
                    if operator_lookup_table[match.group(2)](get_value_by_keystr(var1, context), int(var2)):
                        block_text = match.group(4)
                    if operator_lookup_table[match.group(2)](int(var1), get_value_by_keystr(var1, context)):
                        block_text = match.group(4)
                    if operator_lookup_table[match.group(2)](int(var1), int(var2)):
                        block_text = match.group(4)
                except ValueError:
                    if operator_lookup_table[match.group(2)](get_value_by_keystr(var1, context), var2):
                        block_text = match.group(4)
                    if operator_lookup_table[match.group(2)](var1, get_value_by_keystr(var1, context)):
                        block_text = match.group(4)
                    if operator_lookup_table[match.group(2)](var1, var2):
                        block_text = match.group(4)
        page = page.replace(match.group(), block_text)
    return page


def template_parser(page, context):
    page = for_parser(page, context)
    page = if_parser(page, context)
    # vars
    matches = re.finditer(r"{{(.+)}}", page)
    for match in matches:
        page = page.replace('{{%s}}' % match.group(1), str(get_value_by_keystr(match.group(1), context)))
    return page


def get_page(request):
    context = {
        'item': '123',
        'int': 123,
        'list': [[1, 2], [3], [4]],
        'lis': {'4': True, 2: {'hi': 'Hello'}},
    }
    with open('templates/test.html', 'r') as f:
        page = template_parser(f.read(), context)

    return page.encode()
