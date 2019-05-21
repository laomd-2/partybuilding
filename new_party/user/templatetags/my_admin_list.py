from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def choices(cl, spec):
    return list(spec.choices(cl))


@register.simple_tag
def replace(s, a, b):
    return mark_safe(s.replace(a, b))


@register.simple_tag
def show(cl):
    print(cl.__dict__)


@register.simple_tag
def used_filter_num(cl):
    cnt = 0
    for f in cl.filter_specs:
        if f.used_parameters:
            cnt += 1
    return cnt
