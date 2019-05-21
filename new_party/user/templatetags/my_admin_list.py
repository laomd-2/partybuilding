from django.template import Library

register = Library()


@register.simple_tag
def choices(cl, spec):
    return list(spec.choices(cl))

