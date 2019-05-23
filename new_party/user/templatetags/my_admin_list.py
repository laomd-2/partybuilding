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
    from django.forms.boundfield import BoundField
    from django.contrib.admin.helpers import AdminField
    if not isinstance(cl, dict):
        print(type(cl), cl.__dict__)


@register.simple_tag
def used_filter_num(cl):
    cnt = 0
    for f in cl.filter_specs:
        if f.used_parameters:
            cnt += 1
    return cnt


@register.simple_tag
def get_fields(fieldline):
    form = fieldline.form
    fields = []
    for f in fieldline.fields:
        try:
            fields.append(form[f])
        except:
            pass
    return fields
