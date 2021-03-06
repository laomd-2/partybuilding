from bs4 import BeautifulSoup
from django import template
from django.contrib.admin.views.main import ChangeList
from django.template import Library
from django.utils import six
from django.utils.safestring import mark_safe
from django.utils.html import escape

from xadmin.util import static, vendor as util_vendor

register = Library()


@register.simple_tag(takes_context=True)
def view_block(context, block_name, *args, **kwargs):
    if 'admin_view' not in context:
        return ""

    admin_view = context['admin_view']
    nodes = []
    method_name = 'block_%s' % block_name

    cls_str = str if six.PY3 else basestring
    for view in [admin_view] + admin_view.plugins:
        if hasattr(view, method_name) and callable(getattr(view, method_name)):
            block_func = getattr(view, method_name)
            result = block_func(context, nodes, *args, **kwargs)
            if result and isinstance(result, cls_str):
                nodes.append(result)
    if nodes:
        return mark_safe(''.join(nodes))
    else:
        return ""


@register.filter
def admin_urlname(value, arg):
    return 'xadmin:%s_%s_%s' % (value.app_label, value.model_name, arg)


static = register.simple_tag(static)


@register.simple_tag(takes_context=True)
def vendor(context, *tags):
    return util_vendor(*tags).render()


class BlockcaptureNode(template.Node):
    """https://chriskief.com/2013/11/06/conditional-output-of-a-django-block/"""

    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = escape(output)
        return ''


@register.tag(name='blockcapture')
def do_blockcapture(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'blockcapture' node requires a variable name.")

    nodelist = parser.parse(('endblockcapture',))
    parser.delete_first_token()

    return BlockcaptureNode(nodelist, args)


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""


@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])


@register.simple_tag
def get_height(result_count):
    if result_count > 15:
        return 10 * 37 + 60
    else:
        return 'auto'


@register.simple_tag
def active_next_href(menus):
    i = -1
    for i, li in enumerate(menus):
        if '<li class="active">' in li:
            break
    else:
        i = -1
    return BeautifulSoup(menus[i + 1], 'html.parser').find('a')['href']
