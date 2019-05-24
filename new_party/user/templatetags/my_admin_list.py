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
def class_transform(s):
    class_mapping = {
        'vTextField': 'text-field admintextinputwidget form-control',
        'vDateField': 'date-field admindateinputwidget form-control'
    }
    for k, v in class_mapping.items():
        s = s.replace(k, v)
    return mark_safe(s)


@register.simple_tag
def show(cl):
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
