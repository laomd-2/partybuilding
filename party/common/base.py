import os
import re

from django.conf import settings
from django.contrib.auth import get_permission_codename
from import_export.formats import base_formats


def wrap(value):
    if callable(value):
        value = value()
    if value is None:
        value = ''
    elif value is True:
        value = '是'
    elif value is False:
        value = '否'
    value = str(value)
    if value.startswith('+86'):
        value = value[3:]
    return value


def get_chinese(s):
    pattern = "[\u4e00-\u9fa5]+"
    regex = re.compile(pattern)
    return regex.findall(s)


def get_old(obj):
    model = type(obj)
    try:
        return model.objects.get(pk=obj.pk)
    except model.DoesNotExist:
        return None
    except TypeError:
        return None


class AdminObject(object):
    list_export = []
    list_per_page = 15
    formats = base_formats.DEFAULT_FORMATS[2:3]
    excel_template = os.path.join(settings.MEDIA_ROOT, 'Excel模板/空白.xlsx')

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and \
                self.user.has_perm('%s.%s' % (self.app_label, codename))
